from app.core.utils import make_custom_logger
from app.worker import celery_app, loop
from app.upload.crud import upload_crud
from app.uploader.crud import uploader_crud
from app.video.crud import video_crud, VideoCreate
from app.user.crud import user_crud
from app.db.connect import get_session_context
from app.uploader.utils import normalize_video_resource
# make a custom logger for logging
CUSTOM_LOGGER = make_custom_logger(__name__)

@celery_app.task  # type: ignore
def reconcile_videos():
    """
    Attempts to reconcile/persist video records for orphaned uploads with/(out) buckets
    """
    async def _inner():
        with get_session_context() as session:
            try:
                # get initiated temp upload records
                uploads = await upload_crud.get_by(
                    field="upload_status",
                    value="processing",
                    many=True,
                    session=session,  # type: ignore
                )
                # if there are none, exit task
                if not uploads or (isinstance(uploads, list) and len(uploads) == 0):
                    CUSTOM_LOGGER.info("No uploads found to reconcile")
                    return True

                CUSTOM_LOGGER.info(f"Found uploads: {uploads}")

                # normalize to temp upload records to lists
                if not isinstance(uploads, list):
                    uploads = [uploads]

                # for each record
                for upload in uploads:

                    # create a dump (just a copy in form of a dictionary)
                    upload = upload.model_dump()
                    CUSTOM_LOGGER.info(f"Processing upload: {upload['id']}")

                    # check if video record for upload was already persisted
                    existing_video = await video_crud.get_by(
                        field="upload_hash",
                        value=upload["upload_hash"],
                        session=session,  # type: ignore
                    )

                    # if yes, then delete the temporary upload record, continue for others
                    if existing_video:
                        await upload_crud.delete(id=upload["id"], session=session)  # type: ignore
                        CUSTOM_LOGGER.info(
                            f"Upload already has associated video, skipping: {upload['id']}"
                        )
                        continue

                    # if no, then try to persist by getting the user record of the upload record
                    user = await user_crud.get(id=upload["user_id"], session=session)  # type: ignore

                    # edge check for user, if for some weird reason they don't exist, delete temp upload record, continue
                    if not user:
                        await upload_crud.delete(id=upload["id"], session=session)  # type: ignore
                        CUSTOM_LOGGER.warning(
                            f"User not found for upload: {upload['id']}, user_id: {upload['user_id']}"
                        )
                        continue

                    # if yes, then use user info, bucket info to start creating a new video record, get video bucket resource to be sure
                    uploaded_video = await uploader_crud.get_resource(
                        asset_id=upload["asset_id"]
                    )

                    # if it does not exist, delete temp upload record, continue
                    if uploaded_video is None:
                        await upload_crud.delete(id=upload["id"], session=session)  # type: ignore
                        CUSTOM_LOGGER.warning(
                            f"Uploaded video not found for upload: {upload['id']}, asset_id: {upload['asset_id']}"
                        )
                        continue

                    # create a video record with user info, temp upload info, uploaded video bucket info
                    normalized_data = normalize_video_resource(
                        resource=uploaded_video,
                        upload=upload,
                    )

                    # add video record to db
                    video = await video_crud.upsert(
                        field="upload_hash",
                        value=upload["upload_hash"],
                        data=VideoCreate(**normalized_data),
                        user=user,
                        session=session,  # type: ignore
                    )

                    # if addition was successful
                    if video:
                        #  delete temp upload record
                        await upload_crud.delete(id=upload["id"], session=session)  # type: ignore
                        CUSTOM_LOGGER.info(f"Deleted upload record: {upload['id']}")
                    else:
                        # omit deletion to attempt later
                        CUSTOM_LOGGER.warning(
                            f"Failed to create video for upload: {upload['id']}"
                        )

                CUSTOM_LOGGER.info("Reconcile videos task completed")
                return True  # type: ignore
            except Exception as e:
                CUSTOM_LOGGER.error(f"Error reconciling videos: {e}")
                return False  # type: ignore

    return loop.run_until_complete(_inner())

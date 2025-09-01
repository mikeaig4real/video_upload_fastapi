from app.core.utils import CUSTOM_LOGGER
from app.worker import celery_app, loop
from app.upload.crud import upload_crud
from app.uploader.crud import uploader_crud
from app.video.crud import video_crud, VideoCreate
from app.user.crud import user_crud
from app.db.connect import get_session_context
from app.uploader.utils import normalize_video_resource


@celery_app.task  # type: ignore
def reconcile_videos():
    async def _inner():
        with get_session_context() as session:
            try:
                uploads = await upload_crud.get_by(
                    field="upload_status",
                    value="processing",
                    many=True,
                    session=session,  # type: ignore
                )
                if not uploads or (isinstance(uploads, list) and len(uploads) == 0):
                    CUSTOM_LOGGER.info("No uploads found to reconcile")
                    return True

                CUSTOM_LOGGER.info(f"Found uploads: {uploads}")

                if not isinstance(uploads, list):
                    uploads = [uploads]

                for upload in uploads:
                    upload = upload.model_dump()
                    CUSTOM_LOGGER.info(f"Processing upload: {upload['id']}")

                    existing_video = await video_crud.get_by(
                        field="upload_hash",
                        value=upload["upload_hash"],
                        session=session,  # type: ignore
                    )
                    if existing_video:
                        await upload_crud.delete(id=upload["id"], session=session)  # type: ignore
                        CUSTOM_LOGGER.info(
                            f"Upload already has associated video, skipping: {upload['id']}"
                        )
                        continue

                    user = await user_crud.get(id=upload["user_id"], session=session)  # type: ignore
                    if not user:
                        await upload_crud.delete(id=upload["id"], session=session)  # type: ignore
                        CUSTOM_LOGGER.warning(
                            f"User not found for upload: {upload['id']}, user_id: {upload['user_id']}"
                        )
                        continue

                    uploaded_video = await uploader_crud.get_resource(
                        asset_id=upload["asset_id"]
                    )
                    if uploaded_video is None:
                        await upload_crud.delete(id=upload["id"], session=session)  # type: ignore
                        CUSTOM_LOGGER.warning(
                            f"Uploaded video not found for upload: {upload['id']}, asset_id: {upload['asset_id']}"
                        )
                        continue

                    normalized_data = normalize_video_resource(
                        resource=uploaded_video,
                        upload=upload,
                    )
                    video = await video_crud.upsert(
                        field="upload_hash",
                        value=upload["upload_hash"],
                        data=VideoCreate(**normalized_data),
                        user=user,
                        session=session,  # type: ignore
                    )
                    
                    if video:
                        await upload_crud.delete(id=upload["id"], session=session)  # type: ignore
                        CUSTOM_LOGGER.info(f"Deleted upload record: {upload['id']}")
                    else:
                        CUSTOM_LOGGER.warning(
                            f"Failed to create video for upload: {upload['id']}"
                        )
                        
                CUSTOM_LOGGER.info("Reconcile videos task completed")
                return True  # type: ignore
            except Exception as e:
                CUSTOM_LOGGER.error(f"Error reconciling videos: {e}")
                return False  # type: ignore

    return loop.run_until_complete(_inner())

from typing import Any, Dict, Optional, cast
from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.models.video import UPLOAD_STATUS_ENUM
from app.uploader.crud.cloudinary import CloudinaryResource, DerivedResource

config = get_config()


def findByTransformation(
    transformation: str, derived: list[DerivedResource] | list[dict[str, Any]]
) -> Optional[str]:
    """
    Retrieves thumbnail url of video resource
    """
    if not derived:
        return None
    for item in derived:
        if item.get("transformation") == transformation:
            return item.get("url")
    return None


def normalize_video_resource(
    *, resource: Dict[str, Any], upload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Normalizes resource info based on bucket type
    """
    if upload["upload_provider"] == UPLOAD_BUCKET_ENUM.CLOUDINARY:
        cloudinary_resource = cast(CloudinaryResource, resource)
        return {
            "title": upload["title"],
            "description": upload["description"] or "",
            "duration": upload["duration"],
            "is_public": True,
            "size": upload["size"] or cloudinary_resource.get("bytes"),
            "label": upload["label"],
            "upload_hash": upload["upload_hash"],
            "upload_provider": upload["upload_provider"]
            or UPLOAD_BUCKET_ENUM.CLOUDINARY,
            "asset_id": upload["asset_id"] or cloudinary_resource.get("public_id"),
            "thumbnail_url": findByTransformation(
                upload["eager"], cloudinary_resource.get("derived")
            ),
            # TODO: you have to find how to reconcile playback_url from cloudinary
            "playback_url": cloudinary_resource.get("playback_url", None),
            "type": upload["type"] or cloudinary_resource.get("format"),
            "upload_status": UPLOAD_STATUS_ENUM.COMPLETED,
            "upload_url": cloudinary_resource.get("secure_url")
            or cloudinary_resource.get("url"),
            "height": upload["height"] or cloudinary_resource.get("height"),
            "width": upload["width"] or cloudinary_resource.get("width"),
        }

    elif upload["upload_provider"] == UPLOAD_BUCKET_ENUM.S3:
        return {
            "title": resource.get("Key", "").split("/")[-1],
            "description": "",
            "duration": resource.get("Metadata", {}).get("duration"),  # if stored
            "is_public": True,
            "size": resource.get("Size"),
            "label": upload["label"],
            "upload_hash": resource.get("ETag"),
            "upload_provider": UPLOAD_BUCKET_ENUM.S3,
            "asset_id": resource.get("ETag"),  # or Key
            "thumbnail_url": resource.get("Metadata", {}).get("thumbnail_url"),
            "playback_url": resource.get("Location") or resource.get("url", None),
            "type": None,
            "upload_status": UPLOAD_STATUS_ENUM.COMPLETED,
            "upload_url": resource.get("Location") or resource.get("url"),
        }

    else:
        raise ValueError(f"Unsupported provider: {upload['upload_provider']}")

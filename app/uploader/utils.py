from typing import Any, Dict, Optional
from app.core.config import UPLOAD_BUCKET_ENUM, get_config
from app.models.video import UPLOAD_STATUS_ENUM

config = get_config()

def findByTransformation(transformation: str, derived: Optional[list[dict[str, Any]]]) -> Optional[str]:
    if not derived:
        return None
    for item in derived:
        if item.get("transformation") == transformation:
            return item.get("url")
    return None


def normalize_video_resource(*,
    resource: Dict[str, Any], upload: Dict[str, Any]
) -> Dict[str, Any]:
    if upload['upload_provider'] == UPLOAD_BUCKET_ENUM.CLOUDINARY:
        return {
            "title": upload['title'],
            "description": upload['description'] or "",
            "duration": upload['duration'],
            "is_public": True,
            "size": upload['size'] or resource.get("bytes"),
            "label": upload['label'],
            "upload_hash": upload['upload_hash'],
            "upload_provider": upload['upload_provider'] or UPLOAD_BUCKET_ENUM.CLOUDINARY,
            "asset_id": upload['asset_id'] or resource.get("public_id"),
            "thumbnail_url": findByTransformation(upload['eager'], resource.get("derived")),
            "playback_url": resource.get("secure_url") or resource.get("url"),
            "type": upload['type'] or resource.get("format"),
            "upload_status": UPLOAD_STATUS_ENUM.COMPLETED,
            "upload_url": resource.get("secure_url") or resource.get("url"),
        }

    elif upload['upload_provider'] == UPLOAD_BUCKET_ENUM.S3:
        return {
            "title": resource.get("Key", "").split("/")[-1],
            "description": "",
            "duration": resource.get("Metadata", {}).get("duration"),  # if stored
            "is_public": True,
            "size": resource.get("Size"),
            "label": upload['label'],
            "upload_hash": resource.get("ETag"),
            "upload_provider": UPLOAD_BUCKET_ENUM.S3,
            "asset_id": resource.get("ETag"),  # or Key
            "thumbnail_url": resource.get("Metadata", {}).get("thumbnail_url"),
            "playback_url": resource.get("Location") or resource.get("url"),
            "type": None,
            "upload_status": UPLOAD_STATUS_ENUM.COMPLETED,
            "upload_url": resource.get("Location") or resource.get("url"),
        }

    else:
        raise ValueError(f"Unsupported provider: {upload['upload_provider']}")

import os, uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.core.deps import get_current_admin
from app.core.config import settings

router = APIRouter(prefix="/uploads", tags=["📁 الملفات"])

ALLOWED = {"image/jpeg", "image/png", "image/webp", "image/gif"}


@router.post("/image", dependencies=[Depends(get_current_admin)])
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED:
        raise HTTPException(400, "صيغة الملف غير مدعومة. استخدم JPEG/PNG/WebP/GIF")
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(400, f"حجم الملف يتجاوز الحد المسموح ({settings.MAX_FILE_SIZE // 1_048_576} MB)")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(content)
    return {"url": f"/api/v1/uploads/{filename}", "filename": filename}


@router.get("/{filename}")
def serve_image(filename: str):
    path = os.path.join(settings.UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, "الملف غير موجود")
    return FileResponse(path)

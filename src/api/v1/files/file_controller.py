from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
from fastapi.responses import RedirectResponse

from src.api.v1.files.file_service import FileService
from src.api.v1.auth.auth_service import get_current_user
from src.schemas.response import User, FileUploadResponse
from src.core.exceptions.base import NotFoundException


router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/")
async def upload_handler(
    article_id: int,
    files: list[UploadFile] = File(None),
    file_service: FileService = Depends(),
    current_user: User = Depends(get_current_user),
) -> FileUploadResponse:
    file_urls = await file_service.upload(
        article_id=article_id, user_id=current_user.id, files=files
    )
    return FileUploadResponse(urls=file_urls)


@router.get("/")
async def get_handler(id: int, file_service: FileService = Depends()):
    file_url = await file_service.get_url(id)
    return RedirectResponse(url=file_url)


@router.delete("/")
async def delete_handler(
    id: int,
    file_service: FileService = Depends(),
    current_user: User = Depends(get_current_user),
):
    try:
        await file_service.delete(id, current_user)
        return {"message": f"File with id {id} deleted"}
    except NotFoundException as e:
        raise HTTPException(
            status_code=404, detail={"message": f"File with id {id} not found"}
        ) from e

from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
from fastapi.responses import RedirectResponse

from .file_service import FileService
from ..auth.auth_service import get_current_user
from ..schemas.response import User, FileUploadResponse
from ..exceptions import NotFoundException


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
    file_url = await file_service.get_path(id)
    return RedirectResponse(url=file_url)


@router.get("/info")
async def get_file_info(id: int, file_service: FileService = Depends()):
    file = await file_service.get_file_info(id)
    return {
        "filename": file["filename"],
        "mimetype": file["mimetype"],
        "download_url": f"/files/?id={id}",
    }


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

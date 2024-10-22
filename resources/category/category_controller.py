from fastapi import APIRouter, Body
from typing import List

router = APIRouter(prefix="/categories")


@router.get("/")
async def get_categories_handler():
    return {"categories": []}


@router.get("/{category_id}")
async def get_category_by_id_handler(category_id: int):
    return {"category": {}}


@router.post("/")
async def create_category(name: str = Body(...)):
    # 단일 카테고리 생성 로직
    return {"category": {"name": name}}


@router.post("/multiple")
async def create_multiple_categories(categories: List[str] = Body(...)):
    # 복수 카테고리 생성 로직
    created_categories = [{"name": category} for category in categories]
    return {"categories": created_categories}


@router.post("/select")
async def select_categories(category_ids: List[int] = Body(...)):
    # 복수 카테고리 선택 로직
    return {"selected_categories": category_ids}


@router.put("/select/{user_id}")
async def update_user_categories(user_id: int, category_ids: List[int] = Body(...)):
    # 유저 카테고리 업데이트 로직
    return {"user_id": user_id, "updated_categories": category_ids}


@router.delete("select/{user_id}}")
async def deselect_category(
    user_id: int,
    category_id: int = Body(..., title="ID of the category that will be deselected"),
):
    # 카테고리 삭제 로직
    return {"message": f"Category with id {category_id} deleted"}

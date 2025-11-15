from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

# Մեր մոդուլի ներսից
from app.core.database import get_db
from ..application.services import CategoryService
from ..infrastructure.repositories import CategoryRepository
from ..domain.schemas import Category, CategoryCreate

router = APIRouter(prefix="/category", tags=["Category Management"])
templates = Jinja2Templates(directory="templates")

def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    repository = CategoryRepository(db)
    return CategoryService(repository)

# ====================== API Ծայրակետեր ======================

# 1. Բոլոր Կատեգորիաները (Օգտագործվում է ֆիլտրների համար)
@router.get("/", response_model=List[Category])
async def get_all_categories_api(service: CategoryService = Depends(get_category_service)):
    """Վերադարձնում է բոլոր կատեգորիաները JSON ֆորմատով։"""
    return service.get_all_categories()

# 2. Նոր Կատեգորիա Ստեղծել
@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category_api(
    category_in: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    """Ստեղծում է նոր կատեգորիա։"""
    return service.create_category(category_in)

# 3. Կատեգորիան ID-ով Ստանալ (Շտկված Անուն)
@router.get("/{category_id}", response_model=Category)
async def get_category_by_id_api(
    category_id: int,
    service: CategoryService = Depends(get_category_service)
):
    """Վերադարձնում է կոնկրետ կատեգորիան ID-ով։"""
    return service.get_category_by_id(category_id) # 👈 Այս ֆունկցիան արդեն մշակում է 404-ը

# 4. Կատեգորիան Ջնջել
@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category_api(
    category_id: int,
    service: CategoryService = Depends(get_category_service)
):
    """Ջնջում է կատեգորիան, եթե այն չունի կապակցված ապրանքներ։"""
    return service.delete_category(category_id)
# Իմպորտներ
from fastapi import APIRouter, Depends, Query,Request,status
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from typing import List, Optional
# Մեր կողմից սահմանված ֆայլերի իմպորտ
from app.core.database import get_db
from ..domain.schemas import ProductCreate, Product
from ..application.services import ProductService
from ..infrastructure.repositories import ProductRepository



# APIRouter-ի օբյեկտի ստեղծում
router = APIRouter(prefix="/products", tags=["products"])


# Կախվածությունների (dependencies) ստեղծումը
# Այս մեթոդը կապահովի, որ յուրաքանչյուր հարցման համար ստեղծվի մեկ ProductService
def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repository = ProductRepository(db)
    return ProductService(repository)

# ԹԱՐՄԱՑՆԵԼ /AllProducts ՌՈՈՒՏԵՐԸ (այն, որը կանչում է Ձեր JS-ը)
@router.get("/AllProducts", response_model=List[Product])
async def get_products_filtered_api(
    category_id: Optional[int] = Query(None, alias="category_id"), # 👈 Ավելացնել պարամետրը
    service: ProductService = Depends(get_product_service)
):
    """
    Վերադարձնում է բոլոր ապրանքները կամ զտում ըստ category_id-ի։
    """
    products = service.get_all_products(category_id=category_id)
    return products

@router.get("/create_product", response_class=HTMLResponse, include_in_schema=False)
async def create_product_page(request: Request):
    """
    Ցուցադրում է HTML ձևաթուղթը նոր ապրանք ստեղծելու համար։
    """
    # 1. Templates-ի օբյեկտը ստանում ենք main.py-ից (app.state.templates-ի միջոցով)
    templates = request.app.state.templates

    # 2. Օգտագործում ենք ճիշտ ուղին (որը ցույց է տալիս Ձեր ֆայլի կառուցվածքը)
    return templates.TemplateResponse("products/create_product.html", {"request": request})

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product_api(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    """
    Ստեղծում է նոր ապրանք՝ հիմնվելով ստացված JSON տվյալների վրա։
    """
    new_product = service.create_product(product_data)
    return new_product
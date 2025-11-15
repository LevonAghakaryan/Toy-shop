from fastapi import APIRouter, Depends, status, Header, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.products.infrastructure.repositories import ProductRepository
from app.modules.cart.infrastructure.repositories import CartRepository
from app.modules.cart.application.services import CartService
from app.modules.cart.domain.schemas import CartResponse, CartItemCreate

router = APIRouter(prefix="/cart", tags=["Cart Management (Stateful)"])

# Dependency՝ CartService-ը ստանալու համար
def get_cart_service(db: Session = Depends(get_db)) -> CartService:
    cart_repo = CartRepository(db)
    # Պետք է տրամադրել ProductRepository-ն՝ պահեստը ստուգելու համար
    product_repo = ProductRepository(db)
    return CartService(cart_repo, product_repo)


# Ժամանակավորապես օգտագործում ենք հատուկ Header կամ Cookie
# Իրականում այստեղ կլիներ օգտատիրոջ Authentication
def get_user_identifier(user_id: str = Header(..., alias="X-User-Identifier")) -> str:
    """Ստանում է օգտատիրոջ/սեսիայի ID-ն Header-ից։"""
    return user_id

@router.get("/", response_model=CartResponse)
async def get_user_cart_api(
    user_identifier: str = Depends(get_user_identifier),
    service: CartService = Depends(get_cart_service)
):
    """Բերում է օգտատիրոջ զամբյուղը։"""
    return service.get_cart(user_identifier)

@router.post("/", response_model=CartResponse)
async def add_to_cart_api(
    item_data: CartItemCreate,
    user_identifier: str = Depends(get_user_identifier),
    service: CartService = Depends(get_cart_service)
):
    """Ավելացնում կամ փոփոխում է ապրանքի քանակը զամբյուղում։"""
    return service.add_item_to_cart(user_identifier, item_data)

@router.delete("/{product_id}", response_model=CartResponse)
async def remove_from_cart_api(
    product_id: int,
    user_identifier: str = Depends(get_user_identifier),
    service: CartService = Depends(get_cart_service)
):
    """Հեռացնում է ապրանքը զամբյուղից։"""
    return service.remove_item_from_cart(user_identifier, product_id)
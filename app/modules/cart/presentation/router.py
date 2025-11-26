from fastapi import APIRouter, Depends, status, Header, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.products.infrastructure.repositories import ProductRepository
from app.modules.cart.infrastructure.repositories import CartRepository
from app.modules.cart.application.services import CartService
from app.modules.cart.domain.schemas import CartResponse, CartItemCreate
# ՆՈՐ ԻՄՊՈՐՏ՝ աուտենտիֆիկացված User ID-ն ստանալու համար
from app.modules.users.presentation.router import get_current_user_id

router = APIRouter(prefix="/cart", tags=["Cart Management (Authenticated)"])


def get_cart_service(db: Session = Depends(get_db)) -> CartService:
    cart_repo = CartRepository(db)
    product_repo = ProductRepository(db)
    return CartService(cart_repo, product_repo)


# ՓՈՓՈԽՈՒԹՅՈՒՆ. Օգտագործում ենք մուտք գործած user_id-ն
@router.get("/", response_model=CartResponse)
async def get_user_cart_api(
    user_id: int = Depends(get_current_user_id), # 👈 ՆՈՐ ԿԱԽՎԱԾՈՒԹՅՈՒՆ
    service: CartService = Depends(get_cart_service)
):
    """Բերում է մուտք գործած օգտատիրոջ զամբյուղը։"""
    return service.get_cart(user_id)

# ՓՈՓՈԽՈՒԹՅՈՒՆ. Օգտագործում ենք մուտք գործած user_id-ն
@router.post("/", response_model=CartResponse)
async def add_to_cart_api(
    item_data: CartItemCreate,
    user_id: int = Depends(get_current_user_id), # 👈 ՆՈՐ ԿԱԽՎԱԾՈՒԹՅՈՒՆ
    service: CartService = Depends(get_cart_service)
):
    """Ավելացնում կամ փոփոխում է ապրանքի քանակը զամբյուղում։"""
    return service.add_item_to_cart(user_id, item_data)

# ՓՈՓՈԽՈՒԹՅՈՒՆ. Օգտագործում ենք մուտք գործած user_id-ն
@router.delete("/{product_id}", response_model=CartResponse)
async def remove_from_cart_api(
    product_id: int,
    user_id: int = Depends(get_current_user_id), # 👈 ՆՈՐ ԿԱԽՎԱԾՈՒԹՅՈՒՆ
    service: CartService = Depends(get_cart_service)
):
    """Հեռացնում է ապրանքը զամբյուղից։"""
    return service.remove_item_from_cart(user_id, product_id)
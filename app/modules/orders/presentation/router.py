from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.products.infrastructure.repositories import ProductRepository
from app.modules.orders.infrastructure.repositories import OrderRepository
from app.modules.orders.application.services import OrderService

# Ներմուծում ենք ճիշտ անունները
from app.modules.orders.domain.schemas import Order, OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_user_identifier(user_id: str = Header(..., alias="X-User-Identifier")) -> str:
    """Ստանում է օգտատիրոջ/սեսիայի ID-ն Header-ից։"""
    return user_id


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    # Իմպորտը ֆունկցիայի ներսում՝ շրջանաձև կախվածությունից խուսափելու համար
    from app.modules.cart.infrastructure.repositories import CartRepository

    order_repository = OrderRepository(db)
    product_repository = ProductRepository(db)
    cart_repository = CartRepository(db)

    return OrderService(order_repository, product_repository, cart_repository)


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order_api(
        # ՈՒՂՂՈՒՄ: Տրամադրում ենք լռելյայն արժեք OrderCreate() -ի միջոցով:
        # Սա կլուծի 422 սխալը, եթե հարցման մարմինը դատարկ է։
        order_data: OrderCreate = OrderCreate(),
        user_identifier: str = Depends(get_user_identifier),
        service: OrderService = Depends(get_order_service)
):
    """
    Ստեղծում է նոր պատվեր՝ օգտատիրոջ Backend-ի զամբյուղից։
    """
    # Փոխանցում ենք order_data-ն service-ին
    new_order = service.create_order_from_cart(user_identifier, order_data)
    return new_order
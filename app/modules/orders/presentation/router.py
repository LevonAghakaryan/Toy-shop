from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.products.infrastructure.repositories import ProductRepository
from app.modules.orders.infrastructure.repositories import OrderRepository
from app.modules.orders.application.services import OrderService
from app.modules.orders.domain.schemas import Order, OrderCreate, OrderUpdate
# ՆՈՐ ԻՄՊՈՐՏ՝ աուտենտիֆիկացված User ID-ն ստանալու համար
from app.modules.users.presentation.router import get_current_user_id

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    # Իմպորտը ֆունկցիայի ներսում՝ շրջանաձև կախվածությունից խուսափելու համար
    from app.modules.cart.infrastructure.repositories import CartRepository

    order_repository = OrderRepository(db)
    product_repository = ProductRepository(db)
    cart_repository = CartRepository(db)

    return OrderService(order_repository, product_repository, cart_repository)


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order_api(
        order_data: OrderCreate = OrderCreate(),
        user_id: int = Depends(get_current_user_id), # 👈 ՆՈՐ ԿԱԽՎԱԾՈՒԹՅՈՒՆ
        service: OrderService = Depends(get_order_service)
):
    """
    Ստեղծում է նոր պատվեր՝ մուտք գործած օգտատիրոջ զամբյուղից։
    """
    # Փոխանցում ենք user_id-ն service-ին
    new_order = service.create_order_from_cart(user_id, order_data)
    return new_order
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Ճիշտ իմպորտ Product-ի համար (քանի որ Ձեր մոդուլում այն Product է)
# from app.modules.products.domain.schemas import Product # Այս իմպորտը պետք չէ այստեղ


# 1. Զամբյուղից ստացվող ապրանքի տեսքը (Frontend-ից)
class CartItem(BaseModel):
    product_id: int
    quantity: int


# 2. Պատվեր ստեղծելու հարցումը (Frontend-ից)
class OrderCreate(BaseModel):
    # Այս դաշտերը կարող են դատարկ լինել, եթե User-ի տվյալներն օգտագործվեն
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None


# Պատվերի կարգավիճակը թարմացնելու սխեմա
class OrderUpdate(BaseModel):
    status: str


# 3. Պատվերի ապրանքի վերադարձվող սխեման (Response)
class OrderItem(BaseModel):
    product_name: str
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True


# 4. Պատվերի ընդհանուր վերադարձվող սխեման (Response)
class Order(BaseModel):
    id: int
    user_id: int # 👈 ՆՈՐ ԴԱՇՏ
    total_amount: float
    status: str
    created_at: datetime
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    items: List[OrderItem]

    class Config:
        from_attributes = True
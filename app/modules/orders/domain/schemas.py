from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# Ճիշտ իմպորտ Product-ի համար (քանի որ Ձեր մոդուլում այն Product է)
from app.modules.products.domain.schemas import Product


# 1. Զամբյուղից ստացվող ապրանքի տեսքը (Frontend-ից)
class CartItem(BaseModel):
    product_id: int
    quantity: int


# 2. Պատվեր ստեղծելու հարցումը (Frontend-ից)
class OrderCreate(BaseModel):
    # Ավելացնում ենք դաշտերը, որոնք պետք է գան Frontend-ից
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
    # ՈՒՂՂՈՒՄ: Ջնջում ենք subtotal-ը, քանի որ այն չկա DB մոդելում
    # (Եթե ցանկանում եք այն պահպանել, ապա պետք է ավելացվի DB մոդելում)

    class Config:
        from_attributes = True


# 4. Պատվերի ընդհանուր վերադարձվող սխեման (Response)
class Order(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    # Ավելացնում ենք հաճախորդի դաշտերը
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    items: List[OrderItem]

    class Config:
        from_attributes = True
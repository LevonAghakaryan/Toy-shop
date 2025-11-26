from pydantic import BaseModel
from typing import List, Optional
# Ենթադրենք՝ դուք ունեք այս իմպորտը՝ ապրանքի տվյալների համար
from app.modules.products.domain.schemas import Product


# 1. CartItem-ի սխեմա՝ հարցման համար (Frontend-ից)
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

# 2. CartItem-ի սխեմա՝ պատասխանի համար
class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    subtotal: float
    product: Product # Կամ ProductResponse, եթե այդպիսին կա

    class Config:
        from_attributes = True

# 3. Զամբյուղի հիմնական պատասխանը (Response)
class CartResponse(BaseModel):
    id: int
    # ՓՈՓՈԽՈՒԹՅՈՒՆ. user_identifier: str-ի փոխարեն user_id: int
    user_id: int
    items: List[CartItemResponse]
    total_amount: float

    class Config:
        from_attributes = True
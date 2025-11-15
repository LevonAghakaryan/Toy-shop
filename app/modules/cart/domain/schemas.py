from pydantic import BaseModel, Field
from typing import List, Optional


# --- Input Schemas ---

class CartItemCreate(BaseModel):
    """Զամբյուղին նոր ապրանք ավելացնելու կամ քանակը փոխելու համար։"""
    product_id: int = Field(..., description="Ապրանքի ID")
    quantity: int = Field(..., gt=0, description="Ավելացվող քանակ")


class CartIdentifier(BaseModel):
    """Օգտատիրոջ ինդենտիֆիկատորը։"""
    # Օգտագործելու ենք օգտատիրոջ ID-ի կամ Session Token-ի փոխարեն
    user_id: str = Field(..., description="Օգտատիրոջ ինդենտիֆիկատորը (Session ID)")


# --- Output Schemas ---

class ProductBaseInfo(BaseModel):
    """Միայն այն ինֆորմացիան, որը պետք է CartItem-ի հետ ցուցադրել։"""
    id: int
    name: str
    price: float
    stock_quantity: int
    img_url: Optional[str] = None

    class Config:
        from_attributes = True


class CartItemResponse(BaseModel):
    """CartItem-ի ամբողջական տեսքը (ներառյալ Product-ի տվյալները)։"""
    id: int
    product_id: int
    quantity: int
    product: ProductBaseInfo  # Կապված ապրանքի տվյալները
    subtotal: float  # Այս դաշտը կհաշվարկվի ծառայության մեջ

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Զամբյուղի ամբողջական տեսքը։"""
    id: int
    user_identifier: str
    items: List[CartItemResponse]
    total_amount: float  # Զամբյուղի ընդհանուր գումարը

    class Config:
        from_attributes = True
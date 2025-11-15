from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# --- ՆՈՐ ՍԽԵՄԱՆԵՐ Category-ի ՀԱՄԱՐ ---

class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- Product Սխեմաների ԹԱՐՄԱՑՈՒՄԸ ---

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    img_url: Optional[str] = None
    stock_quantity: int = 0
    # ՆՈՐ ԴԱՇՏ. category_id-ը անհրաժեշտ է ապրանք ստեղծելիս
    category_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    # ՆՈՐ ԴԱՇՏ. Մենք հիմա ակնկալում ենք, որ API-ը կվերադարձնի ամբողջական Category օբյեկտը
    category: Category

    model_config = ConfigDict(from_attributes=True)
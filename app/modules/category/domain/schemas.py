from pydantic import BaseModel, Field
from typing import Optional, List


# Ընդհանուր բազային սխեմա
class CategoryBase(BaseModel):
    name: str = Field(..., example="Խմիչքներ", description="Կատեգորիայի անունը")


# Սխեմա նոր Category ստեղծելու համար (պահանջում է միայն անուն)
class CategoryCreate(CategoryBase):
    pass


# Սխեմա Category-ի ամբողջական տվյալների համար (ներառում է ID)
class Category(CategoryBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True  # Թույլատրել ORM մոդելներից օբյեկտներ ստեղծել

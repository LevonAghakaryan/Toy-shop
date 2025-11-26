from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from app.core.database import Base # Ձեր հիմնական Base-ը
from typing import List

class User(Base):
    """
    Օգտատիրոջ մոդելը՝ աուտենտիֆիկացիայի համար։
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False) # Խնդրում եմ, հիշեք, որ այն պետք է լինի հեշավորված!
    role: Mapped[str] = mapped_column(String(50), default="user", nullable=False)

    # Կապեր (Relationships)
    carts: Mapped[List["Cart"]] = relationship(
        "Cart",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base  # Ենթադրում ենք, որ Base-ը ճիշտ է իմպորտ արվում
from app.modules.products.domain.models import Product
from app.modules.users.domain.models import User  # 👈 ՆՈՐ Իմպորտ


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)

    # ՓՈՓՈԽՈՒԹՅՈՒՆ
    # user_identifier-ի փոխարեն օգտագործում ենք user_id (Օտար Բանալի)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    # Կապ User-ի հետ
    user = relationship("User", back_populates="carts")  # 👈 ՆՈՐ Կապ

class CartItem(Base):
    """Զամբյուղի առանձին ապրանքների մոդելը։"""
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    # Կապ Cart-ի հետ
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)

    # Կապ Product-ի հետ
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity = Column(Integer, default=1, nullable=False)

    # Relationships
    cart = relationship("Cart", back_populates="items")
    # Այս կապը թույլ կտա հեշտությամբ բերել Product-ի տվյալները (գին, անուն, պահեստ)
    product = relationship("Product")
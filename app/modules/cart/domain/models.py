from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base  # Ենթադրում ենք, որ Base-ը ճիշտ է իմպորտ արվում
from app.modules.products.domain.models import Product

class Cart(Base):
    """Զամբյուղի հիմնական մոդելը, որը կապվում է օգտատիրոջ կամ սեսիայի հետ։"""
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    # Ժամանակավորապես օգտագործում ենք String՝ Օգտատիրոջ ID-ի կամ Session Token-ի համար
    # Հետագայում այս դաշտը կփոխվի User ID-ի (ForeignKey)
    user_identifier = Column(String(255), unique=True, index=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Կապ CartItem-ների հետ (Մեկ Cart-ը կարող է ունենալ բազմաթիվ CartItem-ներ)
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


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
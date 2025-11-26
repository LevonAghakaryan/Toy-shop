from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, func, Text
from app.core.database import Base  # Ձեր հիմնական Base-ը
from typing import List
from app.modules.users.domain.models import User  # 👈 ՆՈՐ Իմպորտ


# ----------------- 1. Order (Պատվեր) Մոդելը -----------------
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # ՆՈՐ ԴԱՇՏ. Օտար բանալի դեպի User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)  # 👈 ՆՈՐ ԴԱՇՏ

    total_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # customer_name և customer_address կարող են մնալ, բայց հիմնական կապն User-ի հետ է
    customer_name: Mapped[str] = mapped_column(String(100), nullable=True)
    customer_address: Mapped[str] = mapped_column(Text, nullable=True)

    # Կապը OrderItem-ների հետ
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    # Կապ User-ի հետ
    user: Mapped["User"] = relationship(back_populates="orders")  # 👈 ՆՈՐ Կապ


# ----------------- 2. OrderItem (Պատվերի Ապրանք) Մոդելը -----------------
class OrderItem(Base):
    """
    Կոնկրետ ապրանքը, որը ներառված է պատվերի մեջ:
    Այն պահում է գինը պատվերի պահին (price_at_purchase)։
    """
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Օտար բանալի դեպի Order
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))

    # Օտար բանալի դեպի Product
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    # Պահպանում ենք ապրանքի անունը, որպեսզի պատվերը չկախված լինի ապրանքի փոփոխված անունից
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Քանակը
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Գինը պատվերի պահին (ԿԱՐԵՎՈՐ Է՝ հաշվապահական հաշվառման համար)
    price_at_purchase: Mapped[float] = mapped_column(Float, nullable=False)

    # Կապը Order-ի հետ
    order: Mapped["Order"] = relationship(back_populates="items")

    # Կապը Product-ի հետ
    # product: Mapped["Product"] = relationship() # Կարող եք ավելացնել եթե պետք է բերել բոլոր դաշտերը
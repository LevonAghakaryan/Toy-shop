from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Float, ForeignKey
from app.core.database import Base  # Ենթադրենք Base-ը գտնվում է app.core.database-ում
from typing import Optional, List
from app.modules.category.domain.models import Category



class Product(Base):
    """
    Տվյալների բազայի մոդել ապրանքների համար։
    """
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    img_url: Mapped[str] = mapped_column(String(255), nullable=True)
    stock_quantity = mapped_column(Integer, default=0, nullable=False)
    # ՆՈՐ ԴԱՇՏ. Օտար բանալի
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # ՆՈՐ ԿԱՊ. Relationship-ը Category մոդելի հետ
    category: Mapped["Category"] = relationship(back_populates="products")
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    """
    Category մոդելը, որը պահում է ապրանքների դասակարգումը:
    Այն կապված է Product մոդելին (մեկ Category-ին կարող է պատկանել շատ Product):
    """
    __tablename__ = "categories"

    # Հիմնական դաշտեր
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)

    # Ռելյացիա Product մոդելի հետ
    # 'products' բեքրեֆը թույլ է տալիս Category օբյեկտից մուտք գործել կապակցված ապրանքներին:
    # cascade="all, delete-orphan" ապահովում է, որ եթե Category-ն ջնջվի, ապա
    # դրա հետ կապված Products-ը նույնպես ջնջվեն (մենք կօգտագործենք delete-ի այլ մեթոդ հետագայում,
    # բայց սա լավ պաշտպանիչ մեխանիզմ է)։
    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="joined"  # Միացնում է eager loading-ը
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

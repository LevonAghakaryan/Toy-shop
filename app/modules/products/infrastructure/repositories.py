# Իմպորտներ
from sqlalchemy.orm import Session, joinedload, noload # Ավելացրել ենք joinedload
from sqlalchemy import select
from typing import List, Optional
# Իմպորտում ենք մեր SQLAlchemy մոդելները և Pydantic սխեմաները
# Ենթադրենք models.py ֆայլը գտնվում է .../domain/-ի մեջ
from ..domain.models import Product, Category
from ..domain.schemas import ProductCreate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: ProductCreate) -> Product:
        # Ստուգում, թե արդյոք category_id-ն գոյություն ունի

        # ՓՈՓՈԽՎԱԾ ԿՈԴ
        # Օգտագործում ենք noload(Category.products)-ը կամ noload('*')-ը՝ կապված օբյեկտների բեռնումը կանխելու համար
        statement = (
            select(Category)
            .filter_by(id=product_data.category_id)
            .options(noload('*'))  # 👈 Ամենահուսալի լուծումը՝ անջատել բոլոր eager loading-ները
        )

        category = self.db.scalars(statement).one_or_none()

        if not category:
            raise ValueError(f"Category with ID {product_data.category_id} not found.")

        # ... (մնացած կոդը նույնն է)
        new_product = Product(**product_data.model_dump())
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def get_all_products(self, category_id: Optional[int] = None) -> List[Product]:
        """
        Վերադարձնում է բոլոր ապրանքները կամ զտում ըստ category_id-ի՝ SQLAlchemy 2.0 ոճով։
        """
        # Օգտագործել select() և joinedload
        statement = select(Product).options(joinedload(Product.category))

        # Զտում
        if category_id is not None and category_id != 0:
            statement = statement.filter(Product.category_id == category_id)

        # Կիրառել scalars()-ը և վերադարձնել բոլոր արդյունքները
        products = self.db.scalars(statement).unique().all()
        return products

    # Ստանալ ապրանքը ըստ ID-ի (ԹԱՐՄԱՑՎԱԾ)
    def get_product_by_id(self, product_id: int) -> Product | None:
        statement = select(Product).options(joinedload(Product.category)).filter_by(id=product_id)
        product = self.db.scalars(statement).unique().one_or_none()
        return product

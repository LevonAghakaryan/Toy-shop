from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional

# Իմպորտներ մեր մոդուլից
from app.core.database import Base  # Միայն որպես type hint
from ..domain.models import Category
from ..domain.schemas import CategoryCreate


class CategoryRepository:
    """
    Category-ի տվյալների հետ աշխատանքի շերտ (CRUD գործողություններ)
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Category]:
        """Վերադարձնում է բոլոր կատեգորիաները"""
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Վերադարձնում է կատեգորիան ID-ով"""
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        """Վերադարձնում է կատեգորիան անունով"""
        return self.db.query(Category).filter(Category.name == name).first()

    def create(self, category_in: CategoryCreate) -> Category:
        """Ստեղծում է նոր կատեգորիա"""
        db_category = Category(name=category_in.name)

        try:
            self.db.add(db_category)
            self.db.commit()
            self.db.refresh(db_category)
            return db_category
        except IntegrityError:
            # Մշակում է դեպքը, երբ Category-ի անունը կրկնվում է (UNIQUE constraint)
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Կատեգորիան '{category_in.name}' արդեն գոյություն ունի:"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Կատեգորիան ստեղծելիս սխալ: {e}"
            )

    def delete(self, category: Category):
        """Ջնջում է Category-ն (Product-ները ավտոմատ կջնջվեն cascade-ի շնորհիվ)"""
        self.db.delete(category)
        self.db.commit()

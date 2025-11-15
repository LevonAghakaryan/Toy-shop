from fastapi import HTTPException, status
from typing import List, Optional

# Իմպորտներ մեր մոդուլից
from ..infrastructure.repositories import CategoryRepository
from ..domain.schemas import CategoryCreate, Category


class CategoryService:
    """
    Category-ի բիզնես տրամաբանության շերտ
    """

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def get_all_categories(self) -> List[Category]:
        """Վերադարձնում է բոլոր կատեգորիաները"""
        return self.repository.get_all()

    def get_category_by_id(self, category_id: int) -> Category:
        """
        Վերադարձնում է կատեգորիան ID-ով:
        Գեներացնում է 404 սխալ, եթե չի գտնվել:
        """
        db_category = self.repository.get_by_id(category_id)
        if not db_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Կատեգորիան ID {category_id}-ով չի գտնվել։"
            )
        return db_category

    def create_category(self, category_in: CategoryCreate) -> Category:
        """Ստեղծում է նոր կատեգորիա՝ նախապես ստուգումներ կատարելով"""

        # Քանի որ Repository-ն արդեն մշակում է IntegrityError-ը, մենք ուղղակի կկանչենք create-ը
        return self.repository.create(category_in)

    def delete_category(self, category_id: int):
        """
        Ջնջում է կատեգորիան ID-ով:
        Նախքան ջնջելը ստուգում է, արդյոք այն գոյություն ունի:
        """
        db_category = self.get_category_by_id(category_id)  # Սա արդեն մշակում է 404-ը

        # Բիզնես կանոն. եթե կատեգորիան ունի կապակցված ապրանքներ, թույլ չտալ ջնջել:
        if db_category.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Չի կարելի ջնջել կատեգորիան '{db_category.name}', քանի որ այն ունի {len(db_category.products)} կապակցված ապրանք։"
            )

        self.repository.delete(db_category)
        return {"message": f"Կատեգորիան ID {category_id}-ով հաջողությամբ ջնջվել է։"}

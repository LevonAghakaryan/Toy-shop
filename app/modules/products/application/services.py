# Իմպորտներ
from fastapi import HTTPException, status
from typing import List, Optional
# Իմպորտում ենք մեր repositories և schemas
from ..infrastructure.repositories import ProductRepository
from ..domain.schemas import Product, ProductCreate


# Բիզնես տրամաբանության կլաս
class ProductService:
    # Կլասը ընդունում է repository որպես կախվածություն
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    # Ստեղծել նոր ապրանք (ԹԱՐՄԱՑՎԱԾ)
    def create_product(self, product_data: ProductCreate) -> Product:
        # Նախկինում Դուք ունեիք ստուգում ըստ ID-ի, որը հնարավոր չէ ավտոմատ ID-ի դեպքում։
        # Այս դեպքում կկենտրոնանանք Category-ի սխալի մշակման վրա։

        try:
            # Օգտագործում ենք repository-ն՝ ապրանքը տվյալների բազայում պահպանելու համար
            return self.repository.create_product(product_data)
        except ValueError as e:
            # Եթե repository-ն ValueError է վերադարձնում (օրինակ՝ Category ID-ն գոյություն չունի),
            # մենք այն փոխակերպում ենք FastAPI-ի HTTPException-ի
            if "Category with ID" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
            # Եթե այլ ValueError է, այնուամենայնիվ բարձրացնում ենք
            raise e

            # Ստանալ բոլոր ապրանքները

    def get_all_products(self, category_id: Optional[int] = None) -> List[Product]:
        """
        Վերադարձնում է բոլոր ապրանքները կամ զտում ըստ category_id-ի:
        """
        return self.repository.get_all_products(category_id)
    # Ստանալ ապրանքը ըստ ID-ի
    def get_product_by_id(self, product_id: int) -> Product:
        product = self.repository.get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )
        return product

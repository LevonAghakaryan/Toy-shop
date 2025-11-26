from fastapi import HTTPException, status
from app.modules.cart.infrastructure.repositories import CartRepository
from app.modules.cart.domain.schemas import CartResponse, CartItemResponse, CartItemCreate
from app.modules.products.infrastructure.repositories import ProductRepository

class CartService:
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def _calculate_cart_response(self, cart) -> CartResponse:
        """Օժանդակ ֆունկցիա՝ զամբյուղի գումարը հաշվարկելու և պատասխանը ձևավորելու համար։"""
        # ... (տրամաբանությունը մնում է նույնը, քանի որ կախված չէ User ID-ի տեսակից)
        total_amount = 0.0
        response_items = []

        for item in cart.items:
            if not item.product:
                product = self.product_repository.get_product_by_id(item.product_id)
                if product:
                    item.product = product
                else:
                    continue

            subtotal = item.product.price * item.quantity
            total_amount += subtotal

            item_data = {
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product": item.product,
                "subtotal": subtotal
            }

            response_items.append(CartItemResponse.model_validate(item_data))

        cart_data = {
            "id": cart.id,
            # ՓՈՓՈԽՈՒԹՅՈՒՆ: user_identifier-ի փոխարեն օգտագործում ենք user_id
            "user_id": cart.user_id,
            "items": response_items,
            "total_amount": total_amount
        }

        return CartResponse.model_validate(cart_data)


    # ՓՈՓՈԽՈՒԹՅՈՒՆ: user_identifier-ի փոխարեն user_id: int
    def get_cart(self, user_id: int) -> CartResponse:
        """Բերում է օգտատիրոջ զամբյուղը։"""
        # Օգտագործում ենք նոր մեթոդը
        cart = self.cart_repository.create_or_get_cart(user_id)
        return self._calculate_cart_response(cart)

    # ՓՈՓՈԽՈՒԹՅՈՒՆ: user_identifier-ի փոխարեն user_id: int
    def add_item_to_cart(self, user_id: int, item_data: CartItemCreate) -> CartResponse:
        """Ավելացնում կամ փոփոխում է ապրանքի քանակը։"""

        product = self.product_repository.get_product_by_id(item_data.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ապրանքը չի գտնվել։")

        # Ստուգում ենք պահեստային քանակը
        if item_data.quantity > product.stock_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Առկա է միայն {product.stock_quantity} հատ ապրանք։"
            )

        cart = self.cart_repository.create_or_get_cart(user_id)
        self.cart_repository.add_or_update_item(cart, item_data.product_id, item_data.quantity)

        # Քանի որ փոփոխություն է կատարվել, կրկին բերում ենք զամբյուղը
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        return self._calculate_cart_response(cart)

    # ՓՈՓՈԽՈՒԹՅՈՒՆ: user_identifier-ի փոխարեն user_id: int
    def remove_item_from_cart(self, user_id: int, product_id: int) -> CartResponse:
        """Հեռացնում է ապրանքը զամբյուղից։"""
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            # Քանի որ User-ը մուտք է գործել, նա պետք է ունենա Cart, եթե նույնիսկ այն դատարկ է,
            # բայց մեր `create_or_get_cart`-ը դա կլուծեր։ Սակայն այս դեպքում, եթե User-ը գոյություն ունի,
            # բայց Cart-ը հանկարծակի ջնջվել է, թողնում ենք 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Զամբյուղը չի գտնվել։")

        cart_item = self.cart_repository.get_cart_item(cart.id, product_id)
        if cart_item:
            self.cart_repository.remove_item(cart_item)

        # Թարմացնելուց հետո նորից բերում ենք տվյալները
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        return self._calculate_cart_response(cart)
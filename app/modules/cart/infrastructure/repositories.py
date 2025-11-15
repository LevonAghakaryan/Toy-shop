from sqlalchemy.orm import Session, joinedload
from app.modules.cart.domain.models import Cart, CartItem
from app.modules.products.domain.models import Product # Product-ը հարկավոր է joinedload-ի համար
from typing import Optional

class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cart_by_identifier(self, identifier: str) -> Optional[Cart]:
        """Գտնում է զամբյուղը user_identifier-ի միջոցով (մեր դեպքում՝ session ID-ով)։"""
        return self.db.query(Cart).filter(Cart.user_identifier == identifier).first()

    def get_cart_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        """Գտնում է կոնկրետ ապրանքը զամբյուղում։"""
        return self.db.query(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id
        ).first()

    def create_or_get_cart(self, identifier: str) -> Cart:
        """Ստեղծում է նոր զամբյուղ կամ վերադարձնում առկան։"""
        cart = self.get_cart_by_identifier(identifier)
        if not cart:
            cart = Cart(user_identifier=identifier)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    def add_or_update_item(self, cart: Cart, product_id: int, quantity: int) -> CartItem:
        """Ավելացնում կամ թարմացնում է ապրանքի քանակը զամբյուղում։"""
        cart_item = self.get_cart_item(cart.id, product_id)

        if cart_item:
            cart_item.quantity = quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            self.db.add(cart_item)

        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def remove_item(self, cart_item: CartItem):
        """Հեռացնում է ապրանքը զամբյուղից։"""
        self.db.delete(cart_item)
        self.db.commit()

    def clear_cart(self, cart: Cart):
        """Մաքրում է զամբյուղի բոլոր ապրանքները։"""
        self.db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        self.db.commit()
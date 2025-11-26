from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

# Ներմուծում ենք կախվածությունները
from app.modules.products.infrastructure.repositories import ProductRepository
from app.modules.cart.infrastructure.repositories import CartRepository
from app.modules.orders.infrastructure.repositories import OrderRepository
from app.modules.orders.domain.models import Order, OrderItem
from app.modules.orders.domain.schemas import OrderCreate


class OrderService:
    def __init__(self,
                 order_repository: OrderRepository,
                 product_repository: ProductRepository,
                 cart_repository: CartRepository):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.cart_repository = cart_repository

    # ՓՈՓՈԽՈՒԹՅՈՒՆ: Փոխարինում ենք user_identifier-ը user_id: int-ով
    def create_order_from_cart(self, user_id: int, order_data: Optional[OrderCreate] = None) -> Order:
        """
        Ստեղծում է նոր պատվեր՝ օգտատիրոջ Backend-ի զամբյուղից (Transaction)։
        Նվազեցնում է պահեստը և մաքրում զամբյուղը։
        """
        # 1. Բերել Cart-ի տվյալները (ներառում է CartItem-ները)
        # ՓՈՓՈԽՈՒԹՅՈՒՆ: Օգտագործում ենք CartRepository-ի նոր մեթոդը
        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart or not cart.items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Զամբյուղը դատարկ է կամ չի գտնվել:")

        order_items_list = []
        total_amount = 0.0

        for cart_item in cart.items:
            product = self.product_repository.get_product_by_id(cart_item.product_id)

            # 2. ՎԵՐՋՆԱԿԱՆ ՍՏՈՒԳՈՒՄ
            if not product or product.stock_quantity < cart_item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ապրանք '{product.name if product else cart_item.product_id}' քանակը հանկարծակի նվազել է կամ ապրանքը ջնջվել է։"
                )

            # 3. Stock Reduction (Պահեստի Նվազեցում)
            product.stock_quantity -= cart_item.quantity

            # 4. OrderItem-ի Ստեղծում
            price_at_purchase = product.price
            subtotal = price_at_purchase * cart_item.quantity
            total_amount += subtotal

            order_item = OrderItem(
                product_id=cart_item.product_id,
                product_name=product.name,
                quantity=cart_item.quantity,
                price_at_purchase=price_at_purchase
            )
            order_items_list.append(order_item)

        # 5. Order-ի Ստեղծում
        new_order = Order(
            # ՆՈՐ ԴԱՇՏ. Կապում ենք պատվերը օգտատիրոջ հետ
            user_id=user_id,
            total_amount=total_amount,
            status="Pending",
            items=order_items_list,
            customer_name=order_data.customer_name if order_data else None,
            customer_address=order_data.customer_address if order_data else None,
        )
        final_order = self.order_repository.create_order(new_order)

        # 6. Cart-ի Մաքրում (Միայն հաջող Commit-ից հետո)
        self.cart_repository.clear_cart(cart)

        return final_order
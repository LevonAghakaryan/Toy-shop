from sqlalchemy.orm import Session
from ..domain.models import Order, OrderItem
from typing import List, Optional


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_data: Order) -> Order:
        """
        Պահպանում է Order օբյեկտը և դրա OrderItem-ները տվյալների բազայում։
        """
        self.db.add(order_data)
        self.db.commit()
        self.db.refresh(order_data)
        return order_data

    # Ավելի ուշ կարող եք ավելացնել get_order_by_id կամ get_all_orders մեթոդները
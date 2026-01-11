from decimal import Decimal
from django.utils import timezone


class OrderBuilder:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._user = None
        self._items = []
        self._shipping_address = None
        self._billing_address = None
        self._payment = None
        self._coupon = None
        self._ref_code = None
        self._ordered_date = None
        self._being_delivered = False
        self._received = False
        self._refund_requested = False
        self._refund_granted = False
        return self
    
    def set_user(self, user):
        self._user = user
        return self
    
    def add_item(self, item):
        self._items.append(item)
        return self
    
    def add_items(self, items):
        self._items.extend(items)
        return self
    
    def add_items_from_cart(self, order_items):
        for order_item in order_items:
            self._items.append(order_item)
        return self
    
    def set_shipping_address(self, address):
        self._shipping_address = address
        return self
    
    def set_billing_address(self, address):
        self._billing_address = address
        return self
    
    def use_same_billing_address(self):
        if not self._shipping_address:
            raise ValueError("Shipping address must be set first")
        self._billing_address = self._shipping_address
        return self
    
    def set_payment(self, payment):
        self._payment = payment
        return self
    
    def apply_coupon(self, coupon):
        self._coupon = coupon
        return self
    
    def set_ref_code(self, ref_code):
        self._ref_code = ref_code
        return self
    
    def generate_ref_code(self):
        import random, string
        self._ref_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        return self
    
    def mark_as_being_delivered(self):
        self._being_delivered = True
        return self
    
    def mark_as_received(self):
        self._received = True
        return self
    
    def set_ordered_date(self, date=None):
        self._ordered_date = date or timezone.now()
        return self
    
    def validate(self):
        errors = []
        if not self._user:
            errors.append("User is required")
        if not self._items:
            errors.append("Order must have at least one item")
        if not self._shipping_address:
            errors.append("Shipping address is required")
        if not self._billing_address:
            errors.append("Billing address is required")
        if not self._ref_code:
            errors.append("Reference code is required")
        return errors
    
    def get_total(self):
        total = sum(item.get_total_item_price() for item in self._items)
        if self._coupon:
            total -= self._coupon.amount
        return total
    
    def build(self):
        errors = self.validate()
        if errors:
            raise ValueError(f"Cannot build order: {', '.join(errors)}")
        
        if not self._ordered_date:
            self._ordered_date = timezone.now()
        
        if not self._ref_code:
            self.generate_ref_code()
        
        return {
            'user': self._user,
            'items': self._items,
            'shipping_address': self._shipping_address,
            'billing_address': self._billing_address,
            'payment': self._payment,
            'coupon': self._coupon,
            'ref_code': self._ref_code,
            'ordered_date': self._ordered_date,
            'being_delivered': self._being_delivered,
            'received': self._received,
            'refund_requested': self._refund_requested,
            'refund_granted': self._refund_granted,
            'total': self.get_total()
        }


class OrderDirector:
    
    @staticmethod
    def create_simple_order(builder, user, items, address):
        return (builder
                .set_user(user)
                .add_items(items)
                .set_shipping_address(address)
                .use_same_billing_address()
                .generate_ref_code()
                .set_ordered_date()
                .build())
    
    @staticmethod
    def create_full_order(builder, user, items, shipping_addr, billing_addr, payment, coupon=None):
        builder.set_user(user).add_items(items)
        if coupon:
            builder.apply_coupon(coupon)
        return (builder
                .set_shipping_address(shipping_addr)
                .set_billing_address(billing_addr)
                .set_payment(payment)
                .generate_ref_code()
                .set_ordered_date()
                .build())


class OrderItemBuilder:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._item = None
        self._quantity = 1
        self._ordered = False
        return self
    
    def set_item(self, item):
        self._item = item
        return self
    
    def set_quantity(self, quantity):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self._quantity = quantity
        return self
    
    def mark_as_ordered(self):
        self._ordered = True
        return self
    
    def build(self):
        if not self._item:
            raise ValueError("Item is required")
        return {'item': self._item, 'quantity': self._quantity, 'ordered': self._ordered}


__all__ = ['OrderBuilder', 'OrderDirector', 'OrderItemBuilder']
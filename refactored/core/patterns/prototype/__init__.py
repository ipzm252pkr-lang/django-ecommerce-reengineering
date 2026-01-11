import copy
from django.utils import timezone


class OrderPrototype:
    
    def __init__(self, user, items, shipping_address, billing_address=None):
        self.user = user
        self.items = items
        self.shipping_address = shipping_address
        self.billing_address = billing_address or shipping_address
        self.preferences = {}
        self.created_at = timezone.now()
    
    @classmethod
    def from_order(cls, order):
        items = []
        for order_item in order.items.all():
            items.append({'item': order_item.item, 'quantity': order_item.quantity})
        
        prototype = cls(
            user=order.user,
            items=items,
            shipping_address=order.shipping_address,
            billing_address=order.billing_address
        )
        
        if order.coupon:
            prototype.preferences['coupon_code'] = order.coupon.code
        
        return prototype
    
    def clone(self):
        cloned = copy.deepcopy(self)
        cloned.created_at = timezone.now()
        return cloned
    
    def shallow_clone(self):
        return copy.copy(self)
    
    def to_dict(self):
        return {
            'user': self.user,
            'items': self.items,
            'shipping_address': self.shipping_address,
            'billing_address': self.billing_address,
            'preferences': self.preferences
        }
    
    def __str__(self):
        return f"OrderPrototype for {self.user.username} ({len(self.items)} items)"


class OrderTemplateManager:
    
    def __init__(self):
        self.templates = {}
    
    def register_template(self, name, prototype):
        self.templates[name] = prototype
    
    def create_order(self, template_name):
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        return self.templates[template_name].clone()
    
    def update_template(self, template_name, prototype):
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        self.templates[template_name] = prototype
    
    def delete_template(self, template_name):
        if template_name in self.templates:
            del self.templates[template_name]
    
    def list_templates(self):
        return list(self.templates.keys())
    
    def get_template(self, template_name):
        return self.templates.get(template_name)


class ItemPrototype:
    
    def __init__(self, title, price, category, description=""):
        self.title = title
        self.price = price
        self.category = category
        self.description = description
        self.discount_price = None
        self.label = None
        self.slug = title.lower().replace(" ", "-")
    
    @classmethod
    def from_item(cls, item):
        prototype = cls(item.title, item.price, item.category, item.description)
        prototype.discount_price = item.discount_price
        prototype.label = item.label
        prototype.slug = item.slug
        return prototype
    
    def clone(self):
        return copy.deepcopy(self)
    
    def create_variation(self, **modifications):
        variation = self.clone()
        for key, value in modifications.items():
            if hasattr(variation, key):
                setattr(variation, key, value)
        return variation
    
    def to_dict(self):
        return {
            'title': self.title,
            'price': self.price,
            'category': self.category,
            'description': self.description,
            'discount_price': self.discount_price,
            'label': self.label,
            'slug': self.slug
        }


class ReorderService:
    
    @staticmethod
    def create_reorder_from_order(order):
        prototype = OrderPrototype.from_order(order)
        cloned = prototype.clone()
        return cloned.to_dict()
    
    @staticmethod
    def save_as_template(order, template_name, user):
        prototype = OrderPrototype.from_order(order)
        return prototype


__all__ = ['OrderPrototype', 'OrderTemplateManager', 'ItemPrototype', 'ReorderService']
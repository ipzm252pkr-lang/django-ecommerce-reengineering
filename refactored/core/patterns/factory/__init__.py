from abc import ABC, abstractmethod
from decimal import Decimal


class Product(ABC):
    
    def __init__(self, title, price, description="", slug=None):
        self.title = title
        self.price = Decimal(str(price))
        self.description = description
        self.slug = slug or title.lower().replace(" ", "-")
        self.discount_price = None
        self.image = None
    
    @abstractmethod
    def get_category(self):
        pass
    
    @abstractmethod
    def get_category_label(self):
        pass
    
    @abstractmethod
    def get_details(self):
        pass
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:product', kwargs={'slug': self.slug})
    
    def get_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    
    def __str__(self):
        return f"{self.title} - ${self.get_price()}"


class BookProduct(Product):
    CATEGORY = 'BK'
    
    def __init__(self, title, price, author, pages, isbn=None, description="", slug=None):
        super().__init__(title, price, description, slug)
        self.author = author
        self.pages = pages
        self.isbn = isbn or f"ISBN-{title[:10]}"
    
    def get_category(self):
        return self.CATEGORY
    
    def get_category_label(self):
        return "Books"
    
    def get_details(self):
        return {
            'type': 'Book',
            'author': self.author,
            'pages': self.pages,
            'isbn': self.isbn,
            'price': str(self.get_price()),
            'category': self.get_category_label()
        }


class ElectronicsProduct(Product):
    CATEGORY = 'EL'
    
    def __init__(self, title, price, brand, warranty_months, description="", slug=None):
        super().__init__(title, price, description, slug)
        self.brand = brand
        self.warranty_months = warranty_months
    
    def get_category(self):
        return self.CATEGORY
    
    def get_category_label(self):
        return "Electronics"
    
    def get_details(self):
        return {
            'type': 'Electronics',
            'brand': self.brand,
            'warranty': f"{self.warranty_months} months",
            'price': str(self.get_price()),
            'category': self.get_category_label()
        }


class ClothingProduct(Product):
    CATEGORY = 'CL'
    
    def __init__(self, title, price, size, color, material, description="", slug=None):
        super().__init__(title, price, description, slug)
        self.size = size
        self.color = color
        self.material = material
    
    def get_category(self):
        return self.CATEGORY
    
    def get_category_label(self):
        return "Clothing"
    
    def get_details(self):
        return {
            'type': 'Clothing',
            'size': self.size,
            'color': self.color,
            'material': self.material,
            'price': str(self.get_price()),
            'category': self.get_category_label()
        }


class ProductFactory:
    
    PRODUCT_TYPES = {
        'book': BookProduct,
        'electronics': ElectronicsProduct,
        'clothing': ClothingProduct,
    }
    
    @staticmethod
    def create_product(product_type, **kwargs):
        product_class = ProductFactory.PRODUCT_TYPES.get(product_type)
        
        if not product_class:
            raise ValueError(f"Unknown product type: {product_type}")
        
        return product_class(**kwargs)
    
    @classmethod
    def register_product_type(cls, type_name, product_class):
        if not issubclass(product_class, Product):
            raise TypeError(f"{product_class} must inherit from Product")
        cls.PRODUCT_TYPES[type_name] = product_class
    
    @classmethod
    def get_available_types(cls):
        return list(cls.PRODUCT_TYPES.keys())


__all__ = ['Product', 'BookProduct', 'ElectronicsProduct', 'ClothingProduct', 'ProductFactory']
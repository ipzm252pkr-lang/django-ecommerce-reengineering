import os
import django

# Налаштування Django перед імпортом моделей
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from decimal import Decimal


def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_all_patterns():
    print("\nDjango E-commerce Reengineering - Design Patterns Demo\n")
    
    print_section("1. Singleton Pattern")
    
    from core.patterns.singleton import PaymentConfig
    
    config1 = PaymentConfig()
    config2 = PaymentConfig()
    
    print(f"Config 1: {config1}")
    print(f"Config 2: {config2}")
    print(f"Same instance: {config1 is config2}")
    print(f"Stripe config: {config1.get_stripe_config()}")
    
    print_section("2. Factory Method Pattern")
    
    from core.patterns.factory import ProductFactory
    
    factory = ProductFactory()
    
    book = factory.create_product(
        'book',
        title='Django for Beginners',
        price=39.99,
        author='William Vincent',
        pages=356
    )
    
    laptop = factory.create_product(
        'electronics',
        title='MacBook Pro',
        price=1999.99,
        brand='Apple',
        warranty_months=12
    )
    
    print(f"Book: {book}")
    print(f"Details: {book.get_details()}")
    print(f"\nLaptop: {laptop}")
    print(f"Details: {laptop.get_details()}")
    
    print_section("3. Abstract Factory Pattern")
    
    from core.patterns.abstract_factory import (
        StandardOrderFactory,
        PremiumOrderFactory,
        OrderProcessor
    )
    
    class MockOrder:
        def get_total(self):
            return Decimal('150.00')
        @property
        def ref_code(self):
            return "ORDER-001"
    
    print("Standard Order:")
    standard_factory = StandardOrderFactory()
    standard_processor = OrderProcessor(standard_factory)
    
    print(f"  Payment: {standard_processor.payment.get_processor_name()}")
    print(f"  Shipping: {standard_processor.shipping.get_method_name()}")
    print(f"  Delivery: {standard_processor.shipping.get_delivery_time()}")
    
    print("\nPremium Order:")
    premium_factory = PremiumOrderFactory()
    premium_processor = OrderProcessor(premium_factory)
    
    print(f"  Payment: {premium_processor.payment.get_processor_name()}")
    print(f"  Shipping: {premium_processor.shipping.get_method_name()}")
    print(f"  Delivery: {premium_processor.shipping.get_delivery_time()}")
    
    print_section("4. Builder Pattern")
    
    from core.patterns.builder import OrderBuilder
    
    builder = OrderBuilder()
    
    class MockUser:
        username = "john_doe"
    
    class MockItem:
        def __init__(self, name, price, qty):
            self.name = name
            self.price = price
            self.quantity = qty
        
        def get_total_item_price(self):
            return Decimal(str(self.price)) * self.quantity
    
    mock_items = [
        MockItem("Django Book", 39.99, 2),
        MockItem("Python Course", 99.99, 1)
    ]
    
    try:
        order_data = (builder
                     .set_user(MockUser())
                     .add_items(mock_items)
                     .set_shipping_address("123 Main St")
                     .use_same_billing_address()
                     .generate_ref_code()
                     .set_ordered_date()
                     .build())
        
        print(f"Order created")
        print(f"Ref Code: {order_data['ref_code']}")
        print(f"Items: {len(order_data['items'])}")
        print(f"Total: ${order_data['total']}")
    except Exception as e:
        print(f"Error: {e}")
    
    print_section("5. Prototype Pattern")
    
    from core.patterns.prototype import OrderPrototype, OrderTemplateManager
    
    weekly_order = OrderPrototype(
        user=MockUser(),
        items=[
            {'name': 'Milk', 'price': 4.99, 'quantity': 2},
            {'name': 'Bread', 'price': 3.49, 'quantity': 1},
        ],
        shipping_address="Home"
    )
    
    template_manager = OrderTemplateManager()
    template_manager.register_template("weekly", weekly_order)
    
    print(f"Template saved: {weekly_order}")
    print(f"Items: {len(weekly_order.items)}")
    
    order_week1 = template_manager.create_order("weekly")
    order_week2 = template_manager.create_order("weekly")
    
    order_week2.items.append({'name': 'Eggs', 'price': 5.99, 'quantity': 1})
    
    print(f"Week 1: {len(order_week1.items)} items")
    print(f"Week 2: {len(order_week2.items)} items")
    print(f"Original: {len(weekly_order.items)} items")

    print("\nObject IDs (deep clone verification):")
    print(f"Template ID: {id(weekly_order)}")
    print(f"Week 1 ID: {id(order_week1)}")
    print(f"Week 2 ID: {id(order_week2)}")
    
    print_section("Summary")
    
    print("\nAll 5 design patterns implemented successfully")
    print("Singleton, Factory Method, Abstract Factory, Builder, Prototype")
    print("\nDemo completed\n")


if __name__ == "__main__":
    demo_all_patterns()
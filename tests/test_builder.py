import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings')

import django
from django.conf import settings

if not hasattr(settings, 'STRIPE_SECRET_KEY'):
    settings.STRIPE_SECRET_KEY = 'test_secret_key'

django.setup()

from core.patterns.builder import OrderBuilder
from decimal import Decimal


class MockUser:
    username = "test_user"


class MockItem:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.quantity = qty
    
    def get_total_item_price(self):
        return Decimal(str(self.price)) * self.quantity


class TestBuilderPattern(unittest.TestCase):
    
    def setUp(self):
        self.builder = OrderBuilder()
        self.user = MockUser()
        self.items = [
            MockItem("Item 1", 10.00, 2),
            MockItem("Item 2", 15.00, 1)
        ]
    
    def test_builder_fluent_interface(self):
        print("\n[TEST] Поетапна побудова замовлення через Fluent Interface")
        print("  Крок 1: Встановлюємо користувача")
        print("  Крок 2: Додаємо товари")
        print("  Крок 3: Встановлюємо адресу доставки")
        print("  Крок 4: Використовуємо ту саму адресу для виставлення рахунку")
        print("  Крок 5: Генеруємо reference code")
        print("  Крок 6: Будуємо замовлення")
        
        order = (self.builder
                .set_user(self.user)
                .add_items(self.items)
                .set_shipping_address("Test Address")
                .use_same_billing_address()
                .generate_ref_code()
                .build())
        
        print(f"\n  Створене замовлення:")
        print(f"    Ref Code: {order['ref_code']}")
        print(f"    Кількість товарів: {len(order['items'])}")
        print(f"    Загальна сума: ${order['total']}")
        self.assertEqual(len(order['items']), 2)
        self.assertIsNotNone(order['ref_code'])
        print("  Результат: Замовлення створено через ланцюжок методів")
    
    def test_builder_validation_no_user(self):
        print("\n[TEST] Валідація: спроба створити замовлення без користувача")
        with self.assertRaises(ValueError) as context:
            self.builder.add_items(self.items).build()
        print(f"  Викинуто ValueError: {context.exception}")
        print("  Результат: Builder перевіряє наявність обов'язкових полів")
    
    def test_use_same_billing_without_shipping(self):
        print("\n[TEST] Валідація: спроба встановити billing без shipping адреси")
        with self.assertRaises(ValueError) as context:
            self.builder.use_same_billing_address()
        print(f"  Викинуто ValueError: {context.exception}")
        print("  Результат: Builder перевіряє послідовність операцій")


if __name__ == '__main__':
    unittest.main(verbosity=2)
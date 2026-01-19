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

from core.patterns.factory import ProductFactory, BookProduct, ElectronicsProduct


class TestFactoryMethod(unittest.TestCase):
    
    def setUp(self):
        self.factory = ProductFactory()
    
    def test_create_book_product(self):
        print("\n[TEST] Створення книги через Factory Method")
        book = self.factory.create_product(
            'book',
            title='Test Book',
            price=29.99,
            author='Test Author',
            pages=200
        )
        print(f"  Тип створеного об'єкта: {type(book).__name__}")
        print(f"  Назва: {book.title}")
        print(f"  Автор: {book.author}")
        print(f"  Сторінок: {book.pages}")
        self.assertIsInstance(book, BookProduct)
        self.assertEqual(book.author, 'Test Author')
        print("  Результат: BookProduct має унікальні поля (author, pages)")
    
    def test_create_electronics_product(self):
        print("\n[TEST] Створення електроніки через Factory Method")
        laptop = self.factory.create_product(
            'electronics',
            title='Test Laptop',
            price=999.99,
            brand='TestBrand',
            warranty_months=24
        )
        print(f"  Тип створеного об'єкта: {type(laptop).__name__}")
        print(f"  Назва: {laptop.title}")
        print(f"  Бренд: {laptop.brand}")
        print(f"  Гарантія: {laptop.warranty_months} місяців")
        self.assertIsInstance(laptop, ElectronicsProduct)
        self.assertEqual(laptop.brand, 'TestBrand')
        print("  Результат: ElectronicsProduct має унікальні поля (brand, warranty)")
    
    def test_invalid_product_type(self):
        print("\n[TEST] Обробка помилки при невідомому типі продукту")
        with self.assertRaises(ValueError) as context:
            self.factory.create_product('invalid_type', title='Test', price=10)
        print(f"  Викинуто виняток ValueError: {context.exception}")
        print("  Результат: Фабрика коректно обробляє невідомі типи")


if __name__ == '__main__':
    unittest.main(verbosity=2)
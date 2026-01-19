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
if not hasattr(settings, 'STRIPE_PUBLISHABLE_KEY'):
    settings.STRIPE_PUBLISHABLE_KEY = 'test_public_key'

django.setup()

from core.patterns.singleton import PaymentConfig


class TestSingletonPattern(unittest.TestCase):
    
    def setUp(self):
        PaymentConfig._instance = None
        PaymentConfig._initialized = False
    
    def test_singleton_identity(self):
        print("\n[TEST] Перевірка гарантії єдиного екземпляра Singleton")
        config1 = PaymentConfig()
        config2 = PaymentConfig()
        print(f"  Створено config1 з ID: {id(config1)}")
        print(f"  Створено config2 з ID: {id(config2)}")
        print(f"  Чи однакові об'єкти? {config1 is config2}")
        self.assertIs(config1, config2)
        print("  Результат: config1 та config2 вказують на ОДИН об'єкт у пам'яті")
    
    def test_singleton_has_stripe_key(self):
        print("\n[TEST] Перевірка правильної ініціалізації конфігурації")
        config = PaymentConfig()
        print(f"  Stripe Secret Key: {config.stripe_secret_key}")
        print(f"  Валюта за замовчуванням: {config.currency}")
        self.assertIsNotNone(config.stripe_secret_key)
        self.assertEqual(config.currency, "USD")
        print("  Результат: Конфігурація ініціалізована коректно")
    
    def test_singleton_config_method(self):
        print("\n[TEST] Перевірка методу get_stripe_config()")
        config = PaymentConfig()
        stripe_config = config.get_stripe_config()
        print(f"  Повернута конфігурація: {stripe_config}")
        self.assertIn('secret_key', stripe_config)
        self.assertIn('currency', stripe_config)
        print("  Результат: Метод повертає всі необхідні параметри")


if __name__ == '__main__':
    unittest.main(verbosity=2)
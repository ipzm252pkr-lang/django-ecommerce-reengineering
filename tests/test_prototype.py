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

from core.patterns.prototype import OrderPrototype, OrderTemplateManager


class MockUser:
    username = "test_user"


class TestPrototypePattern(unittest.TestCase):
    
    def test_prototype_clone(self):
        print("\n[TEST] Клонування об'єкта OrderPrototype")
        original = OrderPrototype(
            user=MockUser(),
            items=[{'name': 'Item1', 'qty': 1}],
            shipping_address="Address"
        )
        
        clone = original.clone()
        
        print(f"  Оригінальний об'єкт ID: {id(original)}")
        print(f"  Клонований об'єкт ID: {id(clone)}")
        print(f"  Чи різні об'єкти? {original is not clone}")
        self.assertIsNot(original, clone)
        print("  Результат: Створено новий незалежний об'єкт")
    
    def test_deep_clone_independence(self):
        print("\n[TEST] Незалежність клону від оригіналу (deep copy)")
        original = OrderPrototype(
            user=MockUser(),
            items=[{'name': 'Item1', 'qty': 1}],
            shipping_address="Address"
        )
        
        clone = original.clone()
        
        print(f"  До змін:")
        print(f"    Original має {len(original.items)} товар(ів)")
        print(f"    Clone має {len(clone.items)} товар(ів)")
        
        clone.items.append({'name': 'Item2', 'qty': 2})
        
        print(f"  Після додавання товару до клону:")
        print(f"    Original має {len(original.items)} товар(ів)")
        print(f"    Clone має {len(clone.items)} товар(ів)")
        
        self.assertEqual(len(original.items), 1)
        self.assertEqual(len(clone.items), 2)
        print("  Результат: Зміни в клоні НЕ впливають на оригінал")
    
    def test_template_manager(self):
        print("\n[TEST] Робота менеджера шаблонів OrderTemplateManager")
        manager = OrderTemplateManager()
        prototype = OrderPrototype(
            user=MockUser(),
            items=[{'name': 'Weekly Item'}],
            shipping_address="Home"
        )
        
        print("  Крок 1: Реєструємо шаблон 'weekly'")
        manager.register_template("weekly", prototype)
        
        print("  Крок 2: Створюємо два замовлення з шаблону")
        order1 = manager.create_order("weekly")
        order2 = manager.create_order("weekly")
        
        print(f"  Order1 ID: {id(order1)}")
        print(f"  Order2 ID: {id(order2)}")
        print(f"  Чи різні замовлення? {order1 is not order2}")
        
        self.assertIsNot(order1, order2)
        print("  Результат: Кожне замовлення є незалежним клоном шаблону")


if __name__ == '__main__':
    unittest.main(verbosity=2)
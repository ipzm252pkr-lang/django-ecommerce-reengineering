from abc import ABC, abstractmethod
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
import stripe


class PaymentProcessor(ABC):
    
    @abstractmethod
    def process_payment(self, amount, currency="USD", token=None):
        pass
    
    @abstractmethod
    def refund(self, charge_id, amount=None):
        pass
    
    @abstractmethod
    def get_processor_name(self):
        pass


class ShippingMethod(ABC):
    
    @abstractmethod
    def calculate_cost(self, weight=None, distance=None):
        pass
    
    @abstractmethod
    def get_delivery_time(self):
        pass
    
    @abstractmethod
    def get_method_name(self):
        pass


class NotificationService(ABC):
    
    @abstractmethod
    def send_order_confirmation(self, order, recipient):
        pass


class StripePaymentProcessor(PaymentProcessor):
    
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
    
    def process_payment(self, amount, currency="USD", token=None):
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency=currency,
                source=token
            )
            return {
                'success': True,
                'processor': 'Stripe',
                'charge_id': charge['id'],
                'amount': amount,
                'currency': currency
            }
        except stripe.error.CardError as e:
            return {'success': False, 'error': str(e), 'processor': 'Stripe'}
    
    def refund(self, charge_id, amount=None):
        try:
            refund = stripe.Refund.create(
                charge=charge_id,
                amount=int(amount * 100) if amount else None
            )
            return {'success': True, 'refund_id': refund['id']}
        except stripe.error.StripeError as e:
            return {'success': False, 'error': str(e)}
    
    def get_processor_name(self):
        return "Stripe"


class StandardShipping(ShippingMethod):
    
    def calculate_cost(self, weight=None, distance=None):
        return Decimal('0.00')
    
    def get_delivery_time(self):
        return "5-7 business days"
    
    def get_method_name(self):
        return "Standard Shipping"


class EmailNotificationService(NotificationService):
    
    def send_order_confirmation(self, order, recipient):
        try:
            subject = f"Order Confirmation - {order.ref_code}"
            message = f"Thank you for your order.\n\nOrder Reference: {order.ref_code}\nTotal: ${order.get_total()}"
            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False)
            return {'success': True, 'method': 'email'}
        except Exception as e:
            return {'success': False, 'error': str(e)}


class PayPalPaymentProcessor(PaymentProcessor):
    
    def process_payment(self, amount, currency="USD", token=None):
        return {
            'success': True,
            'processor': 'PayPal',
            'transaction_id': f'PP-{amount}-{token}',
            'amount': amount,
            'currency': currency,
            'fee': amount * Decimal('0.034') + Decimal('0.30')
        }
    
    def refund(self, charge_id, amount=None):
        return {'success': True, 'refund_id': f'REFUND-{charge_id}'}
    
    def get_processor_name(self):
        return "PayPal"


class ExpressShipping(ShippingMethod):
    
    def calculate_cost(self, weight=None, distance=None):
        base = Decimal('15.00')
        if weight:
            base += Decimal(str(weight)) * Decimal('1.00')
        return base
    
    def get_delivery_time(self):
        return "1-2 business days"
    
    def get_method_name(self):
        return "Express Shipping"


class OrderProcessingFactory(ABC):
    
    @abstractmethod
    def create_payment_processor(self):
        pass
    
    @abstractmethod
    def create_shipping_method(self):
        pass
    
    @abstractmethod
    def create_notification_service(self):
        pass


class StandardOrderFactory(OrderProcessingFactory):
    
    def create_payment_processor(self):
        return StripePaymentProcessor()
    
    def create_shipping_method(self):
        return StandardShipping()
    
    def create_notification_service(self):
        return EmailNotificationService()


class PremiumOrderFactory(OrderProcessingFactory):
    
    def create_payment_processor(self):
        return PayPalPaymentProcessor()
    
    def create_shipping_method(self):
        return ExpressShipping()
    
    def create_notification_service(self):
        return EmailNotificationService()


class OrderProcessor:
    
    def __init__(self, factory):
        self.payment = factory.create_payment_processor()
        self.shipping = factory.create_shipping_method()
        self.notification = factory.create_notification_service()
    
    def process_order(self, order, payment_token, user_email):
        payment_result = self.payment.process_payment(
            amount=order.get_total(),
            token=payment_token
        )
        
        if not payment_result['success']:
            return {'success': False, 'error': payment_result.get('error', 'Payment failed')}
        
        shipping_cost = self.shipping.calculate_cost()
        delivery_time = self.shipping.get_delivery_time()
        notification_result = self.notification.send_order_confirmation(order, user_email)
        
        return {
            'success': True,
            'payment': payment_result,
            'shipping': {
                'cost': str(shipping_cost),
                'delivery_time': delivery_time,
                'method': self.shipping.get_method_name()
            },
            'notification': notification_result
        }


__all__ = [
    'PaymentProcessor', 'ShippingMethod', 'NotificationService',
    'StripePaymentProcessor', 'PayPalPaymentProcessor',
    'StandardShipping', 'ExpressShipping', 'EmailNotificationService',
    'OrderProcessingFactory', 'StandardOrderFactory', 'PremiumOrderFactory',
    'OrderProcessor'
]
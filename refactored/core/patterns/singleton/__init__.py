from django.conf import settings


class PaymentConfig:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not PaymentConfig._initialized:
            self.stripe_secret_key = settings.STRIPE_SECRET_KEY
            self.stripe_publishable_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
            self.currency = "USD"
            self.default_charge_description = "Django E-commerce Purchase"
            PaymentConfig._initialized = True
    
    def get_stripe_config(self):
        return {
            'secret_key': self.stripe_secret_key,
            'publishable_key': self.stripe_publishable_key,
            'currency': self.currency
        }
    
    def __str__(self):
        return f"PaymentConfig(currency={self.currency})"


__all__ = ['PaymentConfig']
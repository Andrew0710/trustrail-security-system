from .base_detector import BaseDetector

class StripeDetector(BaseDetector):
    def __init__(self):
        patterns = [r'sk_live_[0-9a-zA-Z]{24}', r'rk_live_[0-9a-zA-Z]{24}']  # Stripe secret keys
        super().__init__('stripe_secret_key', patterns, entropy_check=True)
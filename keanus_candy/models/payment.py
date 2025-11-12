class PaymentMethod:
    """Base class for payment types."""
    
    def __init__(self, method_name: str):
        self.method_name = method_name

    def process_payment(self, amount: float) -> bool:
        """Abstract method to process payments."""
        raise NotImplementedError
    
    def refund(self, amount: float) -> bool:
        """Simulate refunding a payment amount."""
        print(f"Refunding ${amount:.2f} via {self.method_name}...")
        return True


class CreditCard(PaymentMethod):
    """Implements credit card payment."""
    
    def __init__(self, card_number: str, holder_name: str):
        super().__init__("Credit Card")
        self.card_number = card_number
        self.holder_name = holder_name
        
    def validate_card(self) -> bool:
        """Validate that the card number has 16 digits."""
        return len(self.card_number) == 16 and self.card_number.isdigit()

    def process_payment(self, amount: float) -> bool:
        """Process a credit card payment."""
        print(f"Charging ${amount:.2f} to card {self.card_number[-4:]}...")
        return True


class PayPal(PaymentMethod):
    """Implements PayPal payment."""
    
    def __init__(self, email: str):
        super().__init__("PayPal")
        self.email = email

    def process_payment(self, amount: float) -> bool:
        """Process a PayPal payment."""
        print(f"Processing PayPal payment of ${amount:.2f} from {self.email}...")
        return True

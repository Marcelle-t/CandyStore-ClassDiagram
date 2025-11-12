from datetime import datetime
from typing import List

from .person import User
from .product import Candy
from .payment import PaymentMethod


class CartItem:
    """Represents a candy in the cart."""
    
    def __init__(self, candy: Candy, quantity: int):
        self.candy = candy
        self.quantity = quantity

    def subtotal(self):
        """Calculate the subtotal for this cart item."""
        return self.candy.price * self.quantity


class ShoppingCart:
    """User's temporary basket."""
    
    def __init__(self, user: User):
        self.user = user
        self._items: List[CartItem] = []  # Protected: internal state

    def add_item(self, candy: Candy, quantity: int):
        """Add candy to the shopping cart."""
        for item in self._items:
            if item.candy == candy:
                item.quantity += quantity
                return
        self._items.append(CartItem(candy, quantity))

    def calculate_total(self):
        """Calculate the total amount in the cart."""
        return sum(item.subtotal() for item in self._items)

    def create_order(self, payment_method: PaymentMethod) -> "Order":
        """Create an order from the current cart contents."""
        total = self.calculate_total()
        order_items = [OrderItem(i.candy, i.quantity) for i in self._items]
        return Order(self.user, order_items, total, payment_method)
    
    def remove_item(self, candy_name: str):
        """Remove a candy from the cart by name."""
        for item in self._items:
            if item.candy.name.lower() == candy_name.lower():
                self._items.remove(item)
                print(f"Removed {candy_name} from cart.")
                return
        print(f"{candy_name} not found in cart.")

    def view_cart(self):
        """Display current items and total price."""
        if not self._items:
            return "Cart is empty."
        details = [f"{i.candy.name} x{i.quantity} = ${i.subtotal():.2f}" for i in self._items]
        total = self.calculate_total()
        return "\n".join(details) + f"\nTotal: ${total:.2f}"

    def clear(self):
        """Clear all items from the cart."""
        self._items.clear()

    def get_items(self) -> List[CartItem]:
        """Get a copy of the cart items."""
        return self._items.copy()


class Order:
    """Represents a confirmed order."""
    
    order_counter = 1000

    def __init__(self, user: User, items: List["OrderItem"], total_amount: float, payment_method: PaymentMethod):
        self.order_id = Order.order_counter
        Order.order_counter += 1
        self.user = user
        self.items = items
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.status = "Pending"
        self.timestamp = datetime.now()

    def confirm_payment(self):
        """Process payment and mark the order as paid."""
        if self.payment_method.process_payment(self.total_amount):
            self.status = "Paid"
            return True
        else:
            self.status = "Payment Failed"
            return False
        
    def summary(self):
        """Generate a readable order summary."""
        lines = [f"Order #{self.order_id} for {self.user.name}",
                 f"Date: {self.timestamp.strftime('%Y-%m-%d %H:%M')}",
                 f"Status: {self.status}",
                 f"Payment Method: {self.payment_method.method_name}",
                 "Items:"]
        for item in self.items:
            lines.append(f" - {item.candy.name} x{item.quantity} = ${item.subtotal:.2f}")
        lines.append(f"Total: ${self.total_amount:.2f}")
        return "\n".join(lines)
    
    def ship_order(self):
        """Mark the order as shipped."""
        self.status = "Shipped"


class OrderItem:
    """A candy included in an order."""
    
    def __init__(self, candy: Candy, quantity: int):
        self.candy = candy
        self.quantity = quantity
        self.subtotal = candy.price * quantity

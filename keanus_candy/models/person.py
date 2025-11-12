from typing import List, Optional


class Person:
    """Abstract base class for all people in the system."""
    
    def __init__(self, person_id: int, name: str, email: str):
        self.person_id = person_id
        self.name = name
        self.email = email

    def display_info(self):
        return f"{self.name} ({self.email})"


class User(Person):
    """Represents a registered user who can shop."""
    
    def __init__(self, user_id: int, name: str, email: str, password: str):
        super().__init__(user_id, name, email)
        self._password = password  # Protected: sensitive data
        self._orders: List["Order"] = []  # Protected: internal state
        self._cart: Optional["ShoppingCart"] = None  # Protected: internal state

    def login(self, email: str, password: str) -> bool:
        """Authenticate the user."""
        return self.email == email and self._password == password

    def add_to_cart(self, candy: "Candy", quantity: int):
        """Add candy to shopping cart."""
        if not self._cart:
            from .shopping import ShoppingCart
            self._cart = ShoppingCart(self)
        self._cart.add_item(candy, quantity)

    def checkout(self, payment_method: "PaymentMethod"):
        """Convert shopping cart into an order."""
        if not self._cart:
            raise ValueError("Cart is empty")
        order = self._cart.create_order(payment_method)
        self._orders.append(order)
        self._cart.clear()
        return order

    def get_orders(self) -> List["Order"]:
        """Get a copy of the user's orders."""
        return self._orders.copy()

    def get_cart(self) -> Optional["ShoppingCart"]:
        """Get the user's shopping cart."""
        return self._cart
    
    def update_password(self, old_password: str, new_password: str) -> bool:
        """Change password if the old password matches."""
        if self._password == old_password:
            self._password = new_password
            print("Password updated successfully.")
            return True
        print("Password update failed: incorrect current password.")
        return False

    def display_info(self):
        """Display user information with masked email for privacy."""
        masked_email = self.email[0] + "***@" + self.email.split("@")[1]
        return f"User: {self.name}, Contact: {masked_email}"

class Staff(User):
    """Represents store employees — inherits from User."""
    
    def __init__(self, user_id: int, name: str, email: str, password: str, position: str):
        super().__init__(user_id, name, email, password)
        self.position = position

    def update_inventory(self, candy: "Candy", new_quantity: int):
        """Update the quantity of a candy in inventory."""
        candy.quantity = new_quantity

    def view_sales_report(self, orders: List["Order"]):
        """Generate a sales report from a list of orders."""
        total = sum(order.total_amount for order in orders)
        return f"Total sales: ${total:.2f}"

    def view_inventory(self, catalog: "Catalog"):
        """Display all candy items in stock."""
        report = "\n".join([f"{c.name} - {c.quantity} units" for c in catalog.candies])
        return f"Inventory Report:\n{report}"
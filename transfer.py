from datetime import datetime

class Transfer:
    def __init__(self, product_id, quantity, from_location, to_location):
        self.product_id = product_id  
        self.quantity = quantity  
        self.from_location = from_location 
        self.to_location = to_location  
        self.transfer_date = datetime.now()  

    def display_transfer_info(self):
        """Show Details Of Operation."""
        print(f"Transfer of Product ID: {self.product_id}, Quantity: {self.quantity}, "
              f"From: {self.from_location}, To: {self.to_location}, Date: {self.transfer_date}")

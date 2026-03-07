class Customer:
    def __init__(self, id, name, email=None, phone=None, address=None, tax_id=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.tax_id = tax_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "tax_id": self.tax_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            tax_id=data.get("tax_id"),
        )


class CustomerManager:
    def __init__(self):
        self.customers = {}

    def add_customer(self, customer):
        if customer.id in self.customers:
            print("A customer with that ID already exists.")
            return False

        self.customers[customer.id] = customer
        print(f"Customer added: {customer.name}")
        return True

    def get_customer(self, customer_id):
        return self.customers.get(customer_id)

    def get_all_customers(self):
        return self.customers

    def has_customer(self, customer_id):
        return customer_id in self.customers

    def delete_customer(self, customer_id):
        if customer_id not in self.customers:
            print("Customer not found.")
            return False

        deleted_customer = self.customers.pop(customer_id)
        print(f"Customer deleted: {deleted_customer.name}")
        return True

    def list_customers(self):
        if not self.customers:
            print("No customers registered.")
            return

        print("\n--- CUSTOMERS ---")
        for customer in self.customers.values():
            print(
                f"ID: {customer.id} | "
                f"Name: {customer.name} | "
                f"Email: {customer.email or '-'} | "
                f"Phone: {customer.phone or '-'} | "
                f"Tax ID: {customer.tax_id or '-'}"
            )

    def search_by_name(self, name_query):
        results = []
        query = name_query.strip().lower()

        for customer in self.customers.values():
            if query in customer.name.lower():
                results.append(customer)

        return results

    def to_dict_list(self):
        return [customer.to_dict() for customer in self.customers.values()]

    def load_from_dict_list(self, customers_data):
        self.customers = {}

        for item in customers_data:
            customer = Customer.from_dict(item)
            self.customers[customer.id] = customer

    def get_next_customer_id(self):
        if not self.customers:
            return 1
        return max(self.customers.keys()) + 1
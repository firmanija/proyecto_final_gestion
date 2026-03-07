import json
import os
from datetime import datetime


PETTY_CASH_FILE = "petty_cash.json"


class Transaction:
    def __init__(self, employee_id, amount, description, transaction_type, date=None):
        self.employee_id = employee_id
        self.amount = amount
        self.description = description
        self.transaction_type = transaction_type
        self.date = date if date else datetime.now()

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "amount": self.amount,
            "description": self.description,
            "transaction_type": self.transaction_type,
            "date": self.date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            employee_id=data["employee_id"],
            amount=data["amount"],
            description=data["description"],
            transaction_type=data["transaction_type"],
            date=datetime.fromisoformat(data["date"])
        )


class Pettycash:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []
        self.load_from_json()

    def open_cash_register(self, employee_id, initial_amount):
        if initial_amount < 0:
            print("Initial amount cannot be negative.")
            return

        self.balance += initial_amount
        self.transactions.append(
            Transaction(employee_id, initial_amount, "Opening cash balance", "income")
        )

        print(f"Petty cash opened with ${initial_amount:.2f}")
        self.save_to_json()

    def add_income(self, employee_id, amount, description):
        if amount <= 0:
            print("Income amount must be greater than 0.")
            return

        self.balance += amount
        self.transactions.append(
            Transaction(employee_id, amount, description, "income")
        )

        print(f"Income registered: ${amount:.2f} | {description}")
        self.save_to_json()

    def add_expense(self, employee_id, amount, description):
        if amount <= 0:
            print("Expense amount must be greater than 0.")
            return

        if amount > self.balance:
            print("Not enough balance for this expense.")
            return

        self.balance -= amount
        self.transactions.append(
            Transaction(employee_id, -amount, description, "expense")
        )

        print(f"Expense registered: ${amount:.2f} | {description}")
        self.save_to_json()

    def list_transactions(self):
        if not self.transactions:
            print("No transactions registered.")
            return

        print("\n--- PETTY CASH TRANSACTIONS ---")

        for index, trans in enumerate(self.transactions, start=1):
            print(
                f"{index}) "
                f"{trans.date.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{trans.transaction_type.upper()} | "
                f"{trans.description} | "
                f"${trans.amount:.2f} | "
                f"Employee: {trans.employee_id}"
            )

        print(f"\nCurrent balance: ${self.balance:.2f}")

    def modify_transaction(self, index, new_amount, new_description):
        if index < 0 or index >= len(self.transactions):
            print("Invalid transaction.")
            return

        if new_amount <= 0:
            print("Amount must be greater than 0.")
            return

        old_transaction = self.transactions[index]

        self.balance -= old_transaction.amount

        if old_transaction.transaction_type == "expense":
            if new_amount > self.balance:
                self.balance += old_transaction.amount
                print("Not enough balance to modify expense.")
                return
            updated_amount = -new_amount
        else:
            updated_amount = new_amount

        self.balance += updated_amount

        updated_transaction = Transaction(
            old_transaction.employee_id,
            updated_amount,
            new_description,
            old_transaction.transaction_type,
            old_transaction.date
        )

        self.transactions[index] = updated_transaction

        print("Transaction modified.")
        self.save_to_json()

    def delete_transaction(self, index):
        if index < 0 or index >= len(self.transactions):
            print("Invalid transaction.")
            return

        transaction = self.transactions.pop(index)
        self.balance -= transaction.amount

        print(f"Deleted transaction: {transaction.description}")
        self.save_to_json()

    def print_closing_report(self):
        print("\n--- CASH CLOSING REPORT ---")
        print(f"Final balance: ${self.balance:.2f}")
        print("Transactions:")
        self.list_transactions()

    def close_cash_register(self):
        print("Petty cash closed.")
        print(f"Final balance: ${self.balance:.2f}")

        self.transactions = []
        self.balance = 0.0

        self.save_to_json()

    def record_sale_payment(self, amount):
        self.add_income("System", amount, "Cash sale payment")

    # =============================
    # JSON PERSISTENCE
    # =============================

    def save_to_json(self):
        data = {
            "balance": self.balance,
            "transactions": [t.to_dict() for t in self.transactions]
        }

        with open(PETTY_CASH_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        if not os.path.exists(PETTY_CASH_FILE):
            return

        with open(PETTY_CASH_FILE, "r") as f:
            data = json.load(f)

        self.balance = data.get("balance", 0.0)
        self.transactions = [
            Transaction.from_dict(t)
            for t in data.get("transactions", [])
        ]
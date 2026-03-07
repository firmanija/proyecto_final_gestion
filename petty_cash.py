from datetime import datetime


class Transaction:
    def __init__(self, employee_id, amount, description, transaction_type):
        self.employee_id = employee_id
        self.amount = amount
        self.description = description
        self.transaction_type = transaction_type
        self.date = datetime.now()


class Pettycash:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []

    def open_cash_register(self, employee_id, initial_amount):
        """Open cash register with an initial balance."""
        if initial_amount < 0:
            print("Initial amount cannot be negative.")
            return

        self.balance += initial_amount
        self.transactions.append(
            Transaction(
                employee_id,
                initial_amount,
                "Opening cash balance",
                "income"
            )
        )
        print(f"Petty cash box opened with an initial balance of: ${initial_amount:.2f}")

    def add_income(self, employee_id, amount, description):
        """Add income to petty cash."""
        if amount <= 0:
            print("Income amount must be greater than 0.")
            return

        self.balance += amount
        self.transactions.append(
            Transaction(employee_id, amount, description, "income")
        )
        print(f"Income of ${amount:.2f} registered for: {description}")

    def add_expense(self, employee_id, amount, description):
        """Add an expense to petty cash."""
        if amount <= 0:
            print("Expense amount must be greater than 0.")
            return

        if amount > self.balance:
            print("There is not enough money to cover this expense.")
            return

        self.balance -= amount
        self.transactions.append(
            Transaction(employee_id, -amount, description, "expense")
        )
        print(f"Expense of ${amount:.2f} has been registered for: {description}")

    def list_transactions(self):
        """List all petty cash transactions."""
        if not self.transactions:
            print("No transactions registered.")
            return

        print("\nPetty cash transactions:")
        for index, trans in enumerate(self.transactions, start=1):
            print(
                f"{index}) "
                f"{trans.date.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{trans.transaction_type.upper()} | "
                f"{trans.description} | "
                f"${trans.amount:.2f} | "
                f"Employee: {trans.employee_id}"
            )

    def modify_transaction(self, index, new_amount, new_description):
        """Modify a specific transaction using zero-based index."""
        if index < 0 or index >= len(self.transactions):
            print("Invalid transaction.")
            return

        if new_amount <= 0:
            print("Amount must be greater than 0.")
            return

        old_transaction = self.transactions[index]

        # Revert old effect on balance
        self.balance -= old_transaction.amount

        # Apply new effect depending on transaction type
        if old_transaction.transaction_type == "expense":
            if new_amount > self.balance:
                # Restore previous balance effect before leaving
                self.balance += old_transaction.amount
                print("There is not enough money to modify this expense.")
                return
            updated_amount = -new_amount
        else:
            updated_amount = new_amount

        self.balance += updated_amount

        updated_transaction = Transaction(
            old_transaction.employee_id,
            updated_amount,
            new_description,
            old_transaction.transaction_type
        )
        updated_transaction.date = old_transaction.date

        self.transactions[index] = updated_transaction
        print("Transaction has been modified.")

    def delete_transaction(self, index):
        """Delete a specific transaction using zero-based index."""
        if index < 0 or index >= len(self.transactions):
            print("Invalid transaction.")
            return

        transaction = self.transactions.pop(index)
        self.balance -= transaction.amount
        print(f"Deleted transaction: {transaction.description} (${transaction.amount:.2f})")

    def print_closing_report(self):
        """Print fiscal closing report (simulated)."""
        print("\nFiscal day-end Z")
        print(f"Total petty cash balance: ${self.balance:.2f}")
        print("Transactions:")
        self.list_transactions()

    def close_cash_register(self):
        """Close the petty cash register."""
        print("Petty cash closing completed.")
        print(f"Final balance: ${self.balance:.2f}")
        self.transactions = []
        self.balance = 0.0

    def record_sale_payment(self, amount):
        """Register a cash sale payment as income."""
        self.add_income("System", amount, "Sale payment")
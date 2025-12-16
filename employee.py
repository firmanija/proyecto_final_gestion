from datetime import datetime

class Employee:
    def __init__(self, id, name, salary, hourly_wage, position, start_date=None):
        self.id = id
        self.name = name
        self.salary = salary  
        self.hourly_wage = hourly_wage
        self.position = position  
        self.start_date = start_date if start_date else datetime.now()  
        self.commissions = 0  

    def add_commission(self, amount):
        """Add comisions to employee."""
        self.commissions += amount

    def calculate_tenure(self):
        """Calculate tenure of employee in years and days."""
        today = datetime.now()
        tenure = today - self.start_date
        years = tenure.days // 365
        months = (tenure.days % 365) // 30
        return years, months

    def display_info(self):
        """Show all employee data."""
        tenure_years, tenure_months = self.calculate_tenure()
        print(f"ID: {self.id}, Name: {self.name}, Position: {self.position}, "
              f"Salary: {self.salary}, Hourly Wage: {self.hourly_wage}, "
              f"Tenure: {tenure_years} years, {tenure_months} months")

from employee import Employee

# Check if the Employee class can be instantiated
try:
    emp = Employee(1, "Test", 1000)
    print(f"Employee Name: {emp.name}")
except Exception as e:
    print(f"An error occurred: {e}")

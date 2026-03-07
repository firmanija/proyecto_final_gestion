import json
import os
from employee import Employee


EMPLOYEES_FILE = "employees.json"


def load_employees():
    """Load employees from JSON file."""
    if not os.path.exists(EMPLOYEES_FILE):
        return []

    try:
        with open(EMPLOYEES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Employee.from_dict(emp) for emp in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_employees(employees):
    """Save employees to JSON file."""
    with open(EMPLOYEES_FILE, "w", encoding="utf-8") as file:
        json.dump([emp.to_dict() for emp in employees], file, indent=4)


def generate_employee_id(employees):
    """Generate incremental employee ID."""
    if not employees:
        return 1
    return max(emp.id for emp in employees) + 1


def find_employee_by_username(employees, username):
    """Find employee by username."""
    for employee in employees:
        if employee.username.lower() == username.lower():
            return employee
    return None


def register_employee():
    """Register a new employee in the system."""
    employees = load_employees()

    print("\n=== REGISTER NEW EMPLOYEE ===")
    name = input("Enter employee name: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (admin/employee): ").strip().lower()

    if not name or not username or not password:
        print("Error: name, username and password are required.")
        return None

    if role not in ["admin", "employee"]:
        role = "employee"

    existing_employee = find_employee_by_username(employees, username)
    if existing_employee:
        print("Error: username already exists.")
        return None

    new_employee = Employee(
        id=generate_employee_id(employees),
        name=name,
        username=username,
        password_hash=Employee.hash_password(password),
        role=role
    )

    employees.append(new_employee)
    save_employees(employees)

    print(f"Employee '{new_employee.username}' registered successfully.")
    return new_employee


def login():
    """Login an employee."""
    employees = load_employees()

    if not employees:
        print("\nNo employees found. You need to create the first admin user.")
        print("Create the first system user now.\n")
        return register_first_admin()

    print("\n=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    employee = find_employee_by_username(employees, username)

    if not employee:
        print("Error: user not found.")
        return None

    if not employee.verify_password(password):
        print("Error: incorrect password.")
        return None

    print(f"\nWelcome, {employee.name} ({employee.role})")
    return employee


def register_first_admin():
    """Create the first admin if no employees exist yet."""
    employees = load_employees()

    if employees:
        print("Employees already exist. First admin setup is not needed.")
        return None

    print("=== FIRST ADMIN SETUP ===")
    name = input("Enter admin name: ").strip()
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()

    if not name or not username or not password:
        print("Error: name, username and password are required.")
        return None

    admin = Employee(
        id=1,
        name=name,
        username=username,
        password_hash=Employee.hash_password(password),
        role="admin"
    )

    employees.append(admin)
    save_employees(employees)

    print(f"Admin user '{admin.username}' created successfully.")
    return admin


def list_employees():
    """Display all registered employees."""
    employees = load_employees()

    if not employees:
        print("No employees registered.")
        return

    print("\n=== EMPLOYEE LIST ===")
    for employee in employees:
        employee.display_info()
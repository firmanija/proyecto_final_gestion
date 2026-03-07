from datetime import datetime
import hashlib


class Employee:
    def __init__(self, id, name, username, password_hash, role="employee", created_at=None):
        self.id = id
        self.name = name
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def verify_password(self, password):
        """Check if provided password matches stored hash."""
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed == self.password_hash

    @staticmethod
    def hash_password(password):
        """Generate password hash."""
        return hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        """Convert employee to dictionary for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create Employee object from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            username=data["username"],
            password_hash=data["password_hash"],
            role=data.get("role", "employee"),
            created_at=data.get("created_at")
        )

    def display_info(self):
        """Display basic employee info."""
        print(f"ID: {self.id} | Name: {self.name} | Username: {self.username} | Role: {self.role}")
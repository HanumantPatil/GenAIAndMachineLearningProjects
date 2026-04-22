"""UserRole value object — RBAC roles for knowledge base access filtering."""
from enum import Enum


class UserRole(str, Enum):
    EMPLOYEE = "employee"
    IT_ADMIN = "it_admin"

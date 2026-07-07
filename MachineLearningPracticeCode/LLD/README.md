# Low-Level Design (LLD) - Object-Oriented Programming

## Overview

This folder contains implementations of **Low-Level Design (LLD)** principles, focusing on object-oriented programming (OOP) concepts, design patterns, and class design for building scalable and maintainable software systems.

## Contents

- `class.py`: Core OOP class implementations and patterns

## Key Concepts

- **Object-Oriented Programming**: Classes, objects, inheritance, polymorphism
- **SOLID Principles**: Design guidelines for robust code
- **Design Patterns**: Reusable solutions to common problems
- **Encapsulation**: Data hiding and access control
- **Inheritance**: Code reuse through hierarchical relationships
- **Polymorphism**: Objects behaving differently based on context
- **Abstraction**: Hiding complex implementation details

## Prerequisites

```
Python 3.7+
Object-Oriented Programming fundamentals
Design pattern knowledge (helpful)
```

## SOLID Principles

### Single Responsibility Principle (SRP)
```
A class should have only one reason to change
Each class handles one responsibility
```

### Open/Closed Principle (OCP)
```
Open for extension, closed for modification
Extend behavior without changing existing code
```

### Liskov Substitution Principle (LSP)
```
Derived classes must be substitutable for base classes
Subclass objects can replace superclass objects without breaking code
```

### Interface Segregation Principle (ISP)
```
Clients shouldn't depend on interfaces they don't use
Create focused, specific interfaces
```

### Dependency Inversion Principle (DIP)
```
Depend on abstractions, not concretions
High-level modules independent of low-level modules
```

## Core OOP Concepts

### Classes and Objects
```python
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def drive(self):
        return f"Driving {self.brand} {self.model}"

car = Car("Toyota", "Camry")
```

### Inheritance
```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model
```

### Polymorphism
```python
class Animal:
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        return "Woof!"

class Cat(Animal):
    def sound(self):
        return "Meow!"
```

### Encapsulation
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Private
    
    def get_balance(self):
        return self._balance
    
    def deposit(self, amount):
        self._balance += amount
```

## Common Design Patterns

### Creational Patterns

**Singleton**
```
Ensure only one instance of a class exists
Usage: Configuration, logging, database connections
```

**Factory**
```
Create objects without specifying exact classes
Usage: Database connectors, data parsers
```

**Builder**
```
Construct complex objects step-by-step
Usage: Complex object configuration
```

### Structural Patterns

**Adapter**
```
Convert interface to another interface clients expect
Usage: Legacy code integration
```

**Decorator**
```
Add functionality to objects dynamically
Usage: Adding features without changing class
```

**Proxy**
```
Provide placeholder/surrogate for another object
Usage: Lazy loading, access control
```

### Behavioral Patterns

**Observer**
```
Define one-to-many dependencies between objects
Usage: Event handling, notifications
```

**Strategy**
```
Define family of algorithms, make them interchangeable
Usage: Different sorting/payment strategies
```

**Command**
```
Encapsulate request as an object
Usage: Undo/redo functionality, queues
```

## How to Run

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run Python scripts
python class.py
```

## Class Design Best Practices

1. **Single Responsibility**: One class, one reason to change
2. **Clear Interfaces**: Public methods well-defined
3. **Encapsulation**: Hide internal details
4. **Inheritance Hierarchy**: Logical relationships
5. **Composition Over Inheritance**: Flexible design
6. **Dependency Injection**: Loose coupling
7. **Documentation**: Clear docstrings
8. **Testability**: Easily testable components

## Example: Well-Designed Class

```python
class Student:
    """Represents a student with enrollment and grading features."""
    
    def __init__(self, student_id: str, name: str):
        """Initialize student with ID and name."""
        self._id = student_id
        self._name = name
        self._grades = []
    
    @property
    def id(self) -> str:
        """Get student ID."""
        return self._id
    
    @property
    def name(self) -> str:
        """Get student name."""
        return self._name
    
    def add_grade(self, grade: float) -> None:
        """Add a grade for the student."""
        if 0 <= grade <= 100:
            self._grades.append(grade)
        else:
            raise ValueError("Grade must be between 0 and 100")
    
    def get_average(self) -> float:
        """Calculate average grade."""
        if not self._grades:
            return 0
        return sum(self._grades) / len(self._grades)
```

## Common Mistakes to Avoid

✗ **God Classes**: Class doing too much
✗ **Tight Coupling**: Hard to test/modify
✗ **Poor Encapsulation**: Exposing internals
✗ **Deep Hierarchies**: Complex inheritance chains
✗ **Violation of SOLID**: Rigid, fragile design
✗ **Poor Naming**: Unclear class/method names
✗ **No Documentation**: Unclear purpose/usage
✗ **Untestable Code**: Hard to unit test

## Benefits of Good LLD

✓ **Maintainability**: Easy to understand and modify
✓ **Extensibility**: Simple to add new features
✓ **Reusability**: Components reused across projects
✓ **Testability**: Components easily unit-testable
✓ **Scalability**: Handles growth without redesign
✓ **Robustness**: Fewer bugs and side effects
✓ **Performance**: Optimized component interactions
✓ **Collaboration**: Clear contracts between components

## Relationship with Machine Learning

While LLD is primarily OOP-focused, it applies to ML projects:
- **Model Classes**: Encapsulate model logic
- **Data Pipeline Classes**: Manage data flow
- **Configuration Management**: Design patterns for settings
- **Testing**: Unit testing ML components
- **Extensibility**: Adding new algorithms/models
- **Maintainability**: Production ML code quality

## Key Learnings

✓ LLD foundation of production software
✓ SOLID principles guide design decisions
✓ Design patterns solve recurring problems
✓ Good design reduces complexity
✓ Encapsulation improves maintainability
✓ Inheritance requires careful planning
✓ Composition often better than inheritance
✓ Well-designed code is easier to test
✓ Documentation crucial for understanding
✓ Refactoring improves existing design

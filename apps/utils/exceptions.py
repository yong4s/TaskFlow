"""Custom exceptions for the Data Access Layer (DAL)."""


class DALError(Exception):
    """Base exception for all Data Access Layer errors."""
    pass


class ObjectNotFoundError(DALError):
    """Raised when a requested object is not found in the database."""
    
    def __init__(self, model_name: str, identifier: str | int):
        self.model_name = model_name
        self.identifier = identifier
        super().__init__(f'{model_name} with identifier "{identifier}" not found')


class PermissionDeniedError(DALError):
    """Raised when user doesn't have permission to access a resource."""
    
    def __init__(self, message: str = 'Permission denied'):
        super().__init__(message)


class BusinessRuleError(DALError):
    """Raised when a business rule is violated."""
    
    def __init__(self, message: str):
        super().__init__(message)


class ValidationError(DALError):
    """Raised when data validation fails."""
    
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f'Validation error for field "{field}": {message}')
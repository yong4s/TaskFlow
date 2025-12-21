from typing import TYPE_CHECKING, List, Optional

from apps.utils.exceptions import PermissionDeniedError, ValidationError

if TYPE_CHECKING:
    from apps.accounts.models import User
    from .models import Project


class ProjectValidator:
    """Validator for project-related business rules and permissions."""
    
    MAX_NAME_LENGTH = 255
    
    def validate_name_format(self, name: str) -> str:
        name = name.strip()
        
        if not name:
            field = 'name'
            message = 'Project name cannot be empty'
            raise ValidationError(field, message)
        
        if len(name) > self.MAX_NAME_LENGTH:
            field = 'name'
            message = f'Project name too long (max {self.MAX_NAME_LENGTH} characters)'
            raise ValidationError(field, message)
        
        return name
    
    def validate_unique_name(self, existing_projects: List['Project'], name: str, exclude_id: Optional[int] = None):
        name_lower = name.lower()
        
        for project in existing_projects:
            if project.name.lower() == name_lower and project.id != exclude_id:
                field = 'name'
                message = 'Project with this name already exists'
                raise ValidationError(field, message)
    
    def validate_ownership(self, user: 'User', project: 'Project'):
        if project.user != user:
            message = 'You can only access your own projects'
            raise PermissionDeniedError(message)
    
    def validate_create_project(self, user: 'User', name: str, existing_projects: List['Project']) -> str:
        """Complete validation for project creation."""
        clean_name = self.validate_name_format(name)
        self.validate_unique_name(existing_projects, clean_name)
        return clean_name
    
    def validate_update_project(self, user: 'User', project: 'Project', existing_projects: List['Project'], name: str = None) -> Optional[str]:
        """Complete validation for project update."""
        self.validate_ownership(user, project)
        
        if name is not None:
            clean_name = self.validate_name_format(name)
            self.validate_unique_name(existing_projects, clean_name, exclude_id=project.id)
            return clean_name
        
        return None
    
    def validate_delete_project(self, user: 'User', project: 'Project'):
        self.validate_ownership(user, project)
    
    def validate_access_project(self, user: 'User', project: 'Project'):
        self.validate_ownership(user, project)
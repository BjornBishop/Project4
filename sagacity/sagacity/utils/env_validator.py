# sagacity/env_validator.py
import os
from typing import List, Optional

class EnvironmentValidator:
    """Validates environment variables are properly set."""
    
    def __init__(self):
        self.required_vars = {
            'base': [
                'DJANGO_SECRET_KEY',
                'DJANGO_DEBUG',
                'ALLOWED_HOSTS',
                'DB_NAME',
                'DB_USER',
                'DB_PASSWORD',
                'DB_HOST',
                'DB_PORT',
            ],
            'production': [
                'EMAIL_HOST',
                'EMAIL_PORT',
                'EMAIL_HOST_USER',
                'EMAIL_HOST_PASSWORD',
                'SECURE_SSL_REDIRECT',
                'SESSION_COOKIE_SECURE',
                'CSRF_COOKIE_SECURE',
            ]
        }
        
        self.optional_vars = [
            'AUTO_RELOAD',
            'DEVELOPMENT_MODE',
        ]
    
    def validate_environment(self, environment: str = 'base') -> List[str]:
        """
        Validates that all required environment variables are set.
        Returns a list of missing variables.
        """
        missing_vars = []
        vars_to_check = self.required_vars['base']
        
        if environment == 'production':
            vars_to_check.extend(self.required_vars['production'])
        
        for var in vars_to_check:
            if not os.getenv(var):
                missing_vars.append(var)
        
        return missing_vars
    
    def get_environment_status(self) -> dict:
        """Returns the status of all environment variables."""
        status = {
            'missing_required': [],
            'missing_optional': [],
            'is_valid': True
        }
        
        # Check if we're in production
        is_production = os.getenv('DJANGO_DEBUG', 'True').lower() == 'false'
        environment = 'production' if is_production else 'base'
        
        # Validate required variables
        status['missing_required'] = self.validate_environment(environment)
        
        # Check optional variables
        status['missing_optional'] = [
            var for var in self.optional_vars
            if not os.getenv(var)
        ]
        
        # Update validity
        status['is_valid'] = len(status['missing_required']) == 0
        
        return status

# Add this to your settings.py
from .env_validator import EnvironmentValidator

def validate_environment():
    validator = EnvironmentValidator()
    status = validator.get_environment_status()
    
    if not status['is_valid']:
        missing_vars = status['missing_required']
        raise Exception(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            "Please check your .env file and ensure all required variables are set."
        )
    
    if status['missing_optional']:
        print(f"Warning: Missing optional environment variables: {', '.join(status['missing_optional'])}")

# Call this at the end of settings.py
validate_environment()
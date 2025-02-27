from rest_framework.exceptions import (
    ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied
)
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import traceback

def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent API error responses.
    
    Returns a standardized error format:
    {
        "status": "error",
        "message": "Human-readable error message", 
        "fields": {                 # Only included for validation errors
            "field_name": ["Error details"]
        },
        "debug": {                  # Only included when DEBUG=True
            "exception": "Exception class name",
            "detail": "Full exception details",
            "traceback": "Stack trace"
        }
        
    }
    """

    response_data = {
        "status": "error",
        "message": None
    }
    
    status_code = getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Handle authentication errors
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, str):
                response_data["message"] = exc.detail
            elif isinstance(exc.detail, dict) and "detail" in exc.detail:
                response_data["message"] = exc.detail["detail"]
            else:
                response_data["message"] = "Authentication failed"
                if isinstance(exc.detail, dict) or hasattr(exc.detail, '__iter__'):
                    response_data["fields"] = exc.detail
    
    # Handle permission errors
    elif isinstance(exc, PermissionDenied):
        response_data["message"] = str(exc.detail) if isinstance(exc.detail, str) else "Permission denied"
    
    # Handle validation errors
    elif isinstance(exc, ValidationError):
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict) and "non_field_errors" in exc.detail:
                # Non-field errors get promoted to the main message
                response_data["message"] = " ".join(exc.detail["non_field_errors"])
                
                # Include any other field errors
                field_errors = {k: v for k, v in exc.detail.items() if k != "non_field_errors"}
                if field_errors:
                    response_data["fields"] = field_errors
            else:
                response_data["message"] = "Validation failed"
                response_data["fields"] = exc.detail
    
    # Generic fallback for unexpected errors
    elif isinstance(exc,Exception):
        
        response_data["message"] = str(exc) if settings.DEBUG else "Internal Server Error,Try again later"
    else:
        response_data["message"] = "An unexpected error occurred"
    
    if response_data["message"] is None:
        response_data["message"] = "Error occurred"
    
    # Add debug information if DEBUG is True
    # if getattr(settings, 'DEBUG', False):
    #     response_data["debug"] = {
    #         "exception": exc.__class__.__name__,
    #         "detail": str(exc),
    #         "traceback": traceback.format_exc()
    #     }
        
    #     # For non-DRF exceptions that don't have a status_code
    #     if not hasattr(exc, 'status_code'):
    #         response_data["debug"]["note"] = "This is a non-DRF exception that was caught by the custom handler"
    
    return Response(response_data, status=status_code)
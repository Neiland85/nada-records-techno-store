"""
API dependencies package.
"""

from app.api.deps.auth import (AuthService, PermissionChecker, RoleChecker,
                               get_current_active_user, get_current_admin_user,
                               get_current_artist_user, get_current_user,
                               get_current_verified_user, get_db,
                               oauth2_scheme, rate_limit)

__all__ = [
    "AuthService",
    "get_db",
    "get_current_user",
    "get_current_active_user",
    "get_current_verified_user",
    "get_current_admin_user",
    "get_current_artist_user",
    "RoleChecker",
    "PermissionChecker",
    "rate_limit",
    "oauth2_scheme",
]

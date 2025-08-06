"""
API dependencies package.
"""
from app.api.deps.auth import (
    AuthService,
    get_db,
    get_current_user,
    get_current_active_user,
    get_current_verified_user,
    get_current_admin_user,
    get_current_artist_user,
    RoleChecker,
    PermissionChecker,
    rate_limit,
    oauth2_scheme,
)

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
     cursor/configurar-backend-inicial-de-tienda-de-m-sica-908a
]

]
      develop

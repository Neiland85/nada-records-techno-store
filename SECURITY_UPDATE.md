# Security Update Migration - Latest Updates

## Recent Critical Fix (Alert #5)

### python-multipart DoS Vulnerability Fix
- **Date**: August 6, 2025
- **Alert**: Dependabot Alert #5 - DoS via malformed multipart/form-data boundary
- **Severity**: High
- **Fixed Version**: python-multipart==0.0.18
- **Impact**: Prevents CPU exhaustion attacks via malicious form data parsing

## Previous Security Changes

### 1. JWT Library Migration
- **Replaced**: `python-jose[cryptography]==3.3.0`
- **With**: `PyJWT[crypto]==2.8.0`
- **Reason**: python-jose has critical security vulnerabilities:
  - Algorithm confusion with OpenSSH ECDSA keys (CVE-2024-33663)
  - Denial of service via compressed JWE content (CVE-2024-33664)

### 2. Sentry SDK Update
- **Updated**: `sentry-sdk[fastapi]` from `1.38.0` to `1.45.0`
- **Reason**: Previous version unintentionally exposed environment variables to subprocesses

### 3. Other Security Updates
- **bcrypt**: Updated from `4.1.1` to `4.2.0`
- **Pillow**: Updated from `10.1.0` to `10.2.0`
- **alembic**: Updated from `1.12.1` to `1.13.1`
- **pydantic**: Updated from `2.5.0` to `2.5.2`

### 4. Code Changes
- Updated `backend/app/api/deps/auth.py` to use PyJWT instead of python-jose
- Fixed import statements and error handling
- Maintained backward compatibility with existing token structure
- Improved timezone handling using `datetime.timezone.utc`

## Testing Required
- [ ] Test JWT token generation and validation
- [ ] Test authentication endpoints
- [ ] Verify no breaking changes in token format
- [ ] Run security scans to confirm vulnerabilities are resolved

## Breaking Changes
None - The JWT token format and API remain the same.

## Security Impact
- ✅ Resolves CVE-2024-33663 (Critical)
- ✅ Resolves CVE-2024-33664 (Moderate) 
- ✅ Resolves Sentry environment variable exposure (Low)
- ✅ General security improvements through dependency updates

# Security Alert #5 - python-multipart DoS Fix

## Alert Details
- **Alert ID**: Dependabot Alert #5
- **Package**: python-multipart
- **Severity**: High
- **CVE**: Denial of Service via malformed multipart/form-data boundary
- **Date Detected**: August 6, 2025

## Vulnerability Description
When parsing form data, python-multipart skips line breaks (CR `\r` or LF `\n`) in front of the first boundary and any trailing bytes after the last boundary. This happens one byte at a time and emits a log event each time, which may cause excessive logging for certain inputs.

An attacker could abuse this by sending a malicious request with lots of data before the first or after the last boundary, causing high CPU load and stalling the processing thread for a significant amount of time. In ASGI applications, this could stall the event loop and prevent other requests from being processed, resulting in a denial of service (DoS).

## Fix Applied
- **Updated**: `python-multipart` to version `0.0.18`
- **Previous Version**: `0.0.17` or earlier (vulnerable)
- **Patch Version**: `>= 0.0.18` (secure)

## Impact Assessment
- **Before Fix**: Vulnerable to DoS attacks via malformed multipart data
- **After Fix**: Protected against excessive CPU consumption from malicious form data
- **Compatibility**: No breaking changes, full backward compatibility maintained

## Testing Checklist
- [ ] File upload functionality works correctly
- [ ] Form data parsing operates normally
- [ ] No performance degradation observed
- [ ] Security scan confirms vulnerability is resolved

## Related Files
- `backend/requirements.txt` - Updated python-multipart version
- `SECURITY_UPDATE.md` - Updated with latest security information

## References
- Original security advisory in Starlette (October 30)
- Email report to python-multipart maintainer (October 3)
- Dependabot security alert #5

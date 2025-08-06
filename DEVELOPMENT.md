# Nada Records Techno Store - Development Setup

## Project Structure
This project is being set up with the following branch strategy:

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: Feature development branches

## Development Workflow
1. **Create feature branches from `develop` using the following naming conventions:**
   - For features: `feature/<short-description>`
   - For bug fixes: `bugfix/<short-description>`
   - For hotfixes: `hotfix/<short-description>`
2. **Push commits to your feature branch and open a Merge Request (MR) to `develop` when ready.**
   - MR must include a clear description of changes.
   - Assign at least one reviewer.
   - Ensure all CI checks pass before requesting review.
3. **Code Review Process:**
   - Reviewer(s) must approve the MR.
   - Address all comments and suggestions.
   - Squash and merge after approval.
4. **Merge `develop` to `main` for releases.**
   - Ensure release notes are updated.
   - Tag the release in `main`.

## Initial Setup Complete
- ✅ Branch structure created
- ✅ Development environment configured

---
*Setup complete*

# Commit message tags

All commit messages are tagged based on the sections of the project that are affected. Commits that relate to GitLab issues are tagged with the issue number.

## Current

- `admin`: Django admin site
- `api`: Django REST API, including serializers and views
- `css`: stylesheets
- `docs`: documentation
- `docker`: Docker containers for development, staging, and production
- `models`: Django models
- `npm`: JavaScript package dependencies, NPM scripts, and other `package.json` changes
- `other`: Everything else
- `packages`: Python package dependencies
- `refactor`: general refactoring (no features or fixes)
- `settings`: Django settings
- `tasks`: Python utilities run with Invoke
- `templates`: Django templates
- `tests`: backend tests
- `ui`: frontend, including components, state management, and routing
- `urls`: Django URL patterns and routing
- `utils`: Python utility functions
- `views`: Django views, excluding API views (see `api`)
- `webpack`: Webpack

## Replaced

- `fe`: `ui`
- `fe/styles`: `css`
- `frontend`: `ui`
- `scripts`: static script files handled by Django; this was entirely replaced by Webpack
- `store`: frontend state management; merged into `fe`
- `styles`: `css`

This repository contains the code that runs [doktortakes.photos](https://doktortakes.photos).

The application itself doesn't have a name. It implements a highly-opinionated photography portfolio and content management system, with a variety of features:

- Upload photos to albums
- Store albums in other albums
- Front-end content management system (as well as Django's built-in administration system)
- Automatic asynchronous thumbnail generation
- Automatic watermarking of photos
- Album access permissions with user or group granularity
- Search through albums
- Lazy-loading of thumbnail images

# Commit message tags

All commit messages are tagged based on the sections of the app that are affected.

- `admin`: Django admin site
- `api`: Django REST Framework API
- `doc`: documentation
- `fe`: frontend; components (including component stylesheets), state management, and routing
- `models`: Django models
- `other`: Everything else
- `packages`: frontend and backend package dependencies
- `refactor`: general refactoring (no features or fixes)
- `settings`: Django settings
- `styles`: site-wide stylesheets
- `tasks`: Python utilities run with Invoke
- `templates`: Django templates
- `tests`: backend tests
- `urls`: Django URL patterns and routing
- `utils`: Python utility functions
- `views`: Django views (not API views)

## Deprecated

- `frontend`: use `fe` instead
- `scripts`: static script files handled by Django

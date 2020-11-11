# Doktor Takes Photos

This repository contains the code that runs [doktortakes.photos](https://doktortakes.photos), my photography portfolio.

The backend is written in Python using Django and Django REST Framework, and the frontend is written in JavaScript using Vue.

The website implements several features that are specifically designed for my use case.

## Backend
- REST API implemented with Django REST Framework
- Directory-like album structure
- Album access permissions with user and group granularity, and access tokens for guest access
- Automatic asynchronous thumbnail generation
- Automatic watermarking of uploaded photos

## Frontend
- Responsive design
- Lazy-loading of image thumbnails
- Search through all photos by album attributes and common metadata, e.g. album name, image dimensions, and taken date
- Frontend content management system, designed to supplement and eventually replace the built-in Django admin site

# Commit message tags

All commit messages are tagged based on the sections of the project that are affected. Commits that relate to GitLab issues are tagged with the issue number.

- `admin`: Django admin site
- `api`: Django REST API, including serializers and views
- `doc`: documentation
- `fe`: front-end interface, including components, state management, and routing
- `fe/styles`: styles for frontend components
- `models`: Django models
- `npm`: JavaScript package dependencies, NPM scripts, and other `package.json` changes
- `other`: Everything else
- `packages`: Python package dependencies
- `refactor`: general refactoring (no features or fixes)
- `settings`: Django settings
- `styles`: site-wide stylesheets
- `tasks`: Python utilities run with Invoke
- `templates`: Django templates
- `tests`: backend tests
- `urls`: Django URL patterns and routing
- `utils`: Python utility functions
- `views`: Django views, excluding API views (see `api`)
- `webpack`: Webpack

## Deprecated

- `frontend`: see `fe`
- `scripts`: static script files handled by Django; entirely replaced by the Webpack bundle
- `store`: front-end state management; see `fe`

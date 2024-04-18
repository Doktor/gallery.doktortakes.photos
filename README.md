# Doktor Takes Photos

This repository contains the code that runs [gallery.doktortakes.photos](https://gallery.doktortakes.photos), my photography portfolio.

The backend is written in Python using Django and Django REST Framework, and the frontend is written in JavaScript using Vue.

The website implements several features that are specifically designed for my use case.

## Backend
- REST API implemented with Django REST Framework
- Directory-like album structure
- Album access permissions with user and group granularity, and access tokens for guest access
- Automatic asynchronous thumbnail generation

## Frontend
- Responsive design
- Lazy-loading of image thumbnails
- Search through all photos by album attributes and common metadata, e.g. album name, image dimensions, and taken date
- Frontend content management system, designed to supplement and eventually replace the built-in Django admin site

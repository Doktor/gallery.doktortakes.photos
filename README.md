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

## Infrastructure

1. Set up a reverse proxy for the Gunicorn server and a server to host the static files. I currently use Caddy to do both.

```sh
sudo nano /etc/caddy/Caddyfile
```

```caddyfile
gallery.doktortakes.photos {
    handle_path /static/* {
        root * /projects/gallery.doktortakes.photos/static/
        file_server
    }
    
    reverse_proxy localhost:1337
}
```

2. Reload Caddy and verify that it's running without errors.

```sh
sudo systemctl reload caddy
sudo systemctl status caddy
```

## Application

1. Create a `.env.production` file based on `.env.example` and set values for all of the environment variables.

2. Build the Docker container.

```sh
sudo docker compose -f docker-compose.production.yml build
```

3. Copy the collected static files from the container to the local filesystem.

```sh
sudo docker cp gallerydoktortakesphotos-backend-1:/app/api/static.1/. ./static/
```

4. Start the Docker container.

```sh
sudo docker compose -f docker-compose.production.yml up --detach
```

5. To upgrade the application, `git pull` and then follow steps 2, 3, and 4.

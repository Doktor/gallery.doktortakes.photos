CREATE DATABASE "gallery.doktortakes.photos";

CREATE USER photos WITH PASSWORD 'photos';
GRANT ALL PRIVILEGES ON DATABASE "gallery.doktortakes.photos" TO photos;
ALTER DATABASE "gallery.doktortakes.photos" OWNER TO photos;

from django.apps import AppConfig


class PhotosConfig(AppConfig):
    name = 'photos'

    def ready(self):
        from django.urls import register_converter
        from photos.converters import MD5HashConverter

        register_converter(MD5HashConverter, 'md5')

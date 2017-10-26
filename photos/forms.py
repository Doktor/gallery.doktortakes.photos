from django import forms
from django.db.models import Q

from photos.models import Album, Photo


class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        if self.instance:
            query = Q(album=self.instance) | Q(album__parent=self.instance)
            self.fields['cover'].queryset = Photo.objects.filter(query)

    class Meta:
        model = Album
        fields = ['name', 'location', 'description', 'start', 'end',
                  'cover', 'parent']

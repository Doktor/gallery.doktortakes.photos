from django.db import models


RANK_DOMAIN = 'domain'
RANK_KINGDOM = 'kingdom'
RANK_PHYLUM = 'phylum'
RANK_CLASS = 'class'
RANK_ORDER = 'order'
RANK_FAMILY = 'family'
RANK_GENUS = 'genus'
RANK_SPECIES = 'species'

TAXON_RANKS = (
    (RANK_DOMAIN, 'Domain'),
    (RANK_KINGDOM, 'Kingdom'),
    (RANK_PHYLUM, 'Phylum'),
    (RANK_CLASS, 'Class'),
    (RANK_ORDER, 'Order'),
    (RANK_FAMILY, 'Family'),
    (RANK_GENUS, 'Genus'),
    (RANK_SPECIES, 'Species'),
)

class Taxon(models.Model):
    catalog_id = models.CharField(max_length=10, unique=True, help_text='Catalogue of Life identifier')

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    rank = models.CharField(max_length=50, choices=TAXON_RANKS, default=RANK_SPECIES)

    common_name = models.CharField(max_length=200, blank=True)

    parent = models.ForeignKey('Taxon', models.SET_NULL, related_name='children', null=True, blank=True)
    parent_catalog_id = models.CharField(max_length=10, help_text='Catalogue of Life identifier')

    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return f'{self.rank}: {self.name}'

    class Meta:
        verbose_name_plural = "taxa"

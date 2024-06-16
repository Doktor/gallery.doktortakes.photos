from django.utils.text import slugify
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.models import Taxon
from photos.models.taxon import TAXON_RANKS
from photos.api.serializers import TaxonSerializer

from http import HTTPStatus as Status
import requests


class ManageTaxonList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request: Request) -> Response:
        serializer = TaxonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=Status.CREATED)

        return Response(serializer.errors, status=Status.BAD_REQUEST)


BASE_URL = 'https://api.checklistbank.org'
DATASET_KEY = 9923


class InvalidCatalogIdError(Exception):
    def __init__(self, catalog_id):
        super().__init__()
        self.catalog_id = catalog_id


class ImportTaxon(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request: Request) -> Response:
        catalog_id = request.data['catalogId']

        try:
            taxon = populate_taxon(catalog_id)
        except InvalidCatalogIdError as e:
            return Response(f"Invalid catalog ID: {e.catalog_id}", status=Status.BAD_REQUEST)

        serializer = TaxonSerializer(taxon)
        return Response(serializer.data, status=Status.OK)


def populate_taxon(catalog_id):
    base_taxon = None
    previous_taxon = None

    while True:
        print('processing', catalog_id)
        taxon, parent_id, created = get_or_create_taxon(catalog_id)

        if base_taxon is None:
            base_taxon = taxon

        # We reached the top level
        if parent_id is None:
            break

        if taxon is None:
            catalog_id = parent_id
            continue

        if previous_taxon is not None:
            previous_taxon.parent = taxon
            previous_taxon.save()

        # We didn't create a new taxon object, which means we processed the
        # parent taxa previously and don't have to process them again
        if not created:
            break

        previous_taxon = taxon
        catalog_id = parent_id

    return base_taxon


def get_taxon_from_catalog(catalog_id):
    response = requests.get(f'{BASE_URL}/dataset/{DATASET_KEY}/taxon/{catalog_id}/info')

    if response.status_code != Status.OK:
        raise InvalidCatalogIdError(catalog_id)

    return response.json()


def get_or_create_taxon(catalog_id):
    try:
        taxon = Taxon.objects.get(catalog_id=catalog_id)
    except Taxon.DoesNotExist:
        pass
    else:
        return taxon, taxon.parent_catalog_id, False

    response = get_taxon_from_catalog(catalog_id)

    parent_id = response['taxon'].get('parentId', None)
    rank = response['taxon']['name']['rank']

    # Skip intermediate taxonomic ranks
    if rank not in [item[0] for item in TAXON_RANKS]:
        return None, parent_id, False

    taxon = Taxon()
    taxon.catalog_id = response['taxon']['id']
    taxon.parent_catalog_id = parent_id
    taxon.name = response['taxon']['name']['scientificName']
    taxon.slug = slugify(taxon.name)
    taxon.rank = rank
    taxon.common_name = get_common_name(response.get('vernacularNames', []))
    taxon.save()

    return taxon, parent_id, True


def get_common_name(names):
    return '; '.join([name['name'] for name in names if name['language'] == 'eng'])

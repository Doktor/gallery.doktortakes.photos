from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET, require_POST

import datetime
import pytz

from photos.api.utils import APIError, get_photo_from_request, api_wrapper
from photos.models import Photo, generate_md5_hash
from photos.settings import ITEMS_PER_PAGE, ITEMS_IN_FILMSTRIP
from photos.views import get_album_by_path, get_photo


def get_photo_by_hash(path, md5):
    try:
        return get_photo(path, md5)
    except Photo.DoesNotExist:
        raise APIError("The specified photo doesn't exist.")


def format_f_stop(f):
    """Takes an f-stop as a fractional string and converts it to a number."""
    try:
        f = f.split('/')
    except AttributeError:
        return 0
    else:
        if len(f) == 2:
            return int(f[0]) / int(f[1])
        else:
            return f[0]


def get_exif(p):
    e = p.exif

    camera = e.get('Image Model', 'Camera unknown')

    try:
        make = e.get('EXIF LensMake', e['Image Make'])
        model = e['EXIF LensModel']

        lens = f'{make} {model}'
    except KeyError:
        lens = 'Lens unknown'

    if 'EF-S' in lens:
        lens = lens.replace('EF-S', 'EF-S ')
    elif 'EF' in lens:
        lens = lens.replace('EF', 'EF ')

    try:
        shutter_speed = f"{e['EXIF ExposureTime']} s"
    except KeyError:
        shutter_speed = 'Unknown'

    try:
        f_stop = f"f/{format_f_stop(e['EXIF FNumber'])}"
    except KeyError:
        if camera != 'Camera unknown':
            f_stop = 'f/0'
        else:
            f_stop = 'Unknown'

    try:
        iso_speed = f"ISO {e['EXIF ISOSpeedRatings']}"
    except KeyError:
        iso_speed = 'Unknown'

    return {
        'camera': camera,
        'lens': lens,
        'shutter_speed': shutter_speed,
        'aperture': f_stop,
        'iso_speed': iso_speed,
    }


def get_index(photo):
    photos = photo.album.photos.all()

    for i, item in enumerate(photos):
        if item.md5 == photo.md5:
            return i
    else:
        raise RuntimeError


def generate_photo_dict(photo, index=None, metadata=True, filmstrip=True):
    taken = photo.taken.astimezone(pytz.timezone(photo.album.timezone))

    response = {
        'image_url': photo.image.url,
        'thumbnail_url': photo.thumbnail.url,
        'square_thumbnail_url': photo.square_thumbnail.url,
        'url': photo.get_absolute_url(),
    }

    if metadata:
        if index is None:
            index = get_index(photo)

        response.update({
            'metadata': {
                'index': index,
                'taken': taken.strftime("%A, %Y-%m-%d, %-I:%M:%S %p"),
                'width': photo.width,
                'height': photo.height,
                'md5': photo.md5,
                'new_tab': photo.image.url,
                'download': reverse(
                    'download', args=[photo.get_path(), photo.md5]),
            },
            'exif': get_exif(photo)
        })

    if filmstrip:
        response['filmstrip'] = generate_filmstrip(photo)

    return response


def generate_filmstrip(photo):
    count = ITEMS_IN_FILMSTRIP
    half = count // 2

    album = photo.album
    all_photos = album.photos.all()

    if all_photos.count() <= count:
        photos = [*all_photos]
    else:
        # Queries
        left_q = Q(taken__lt=photo.taken) & (~Q(pk=photo.pk))
        middle_q1 = Q(taken=photo.taken, uploaded__lt=photo.uploaded)
        middle_q2 = Q(taken=photo.taken, uploaded__gt=photo.uploaded)
        right_q = Q(taken__gt=photo.taken) & (~Q(pk=photo.pk))

        # Filter...
        left = all_photos.filter(left_q).reverse()
        middle_1 = all_photos.filter(middle_q1)
        middle_2 = all_photos.filter(middle_q2)
        right = all_photos.filter(right_q)

        # Join the outside and middle queries
        left = [*left, *middle_1]
        right = [*middle_2, *right]
        lc, rc = len(left), len(right)

        if lc < half:
            deficit = count - 1 - lc
            photos = [*left, photo, *right[:deficit]]
        elif rc < half:
            deficit = count - 1 - rc
            photos = [*left[:deficit], photo, *right]
        else:
            photos = [*left[:half], photo, *right[:half]]

    photos = sorted(photos, key=lambda p: (p.taken, p.pk))

    result = []

    for photo in photos:
        result.append({
            'md5': photo.md5,
            'url': photo.square_thumbnail.url,
            'index': get_index(photo),
        })

    return result


def photo_to_response(photo):
    return JsonResponse(generate_photo_dict(photo))


class PhotoView(View):
    def get(self, request, path):
        try:
            photo = get_photo_from_request(request, path)
        except APIError as e:
            return e.to_response()

        return photo_to_response(photo)

    @method_decorator(login_required)
    def delete(self, request, path):
        try:
            photo = get_photo_from_request(request, path)
        except APIError as e:
            return e.to_response()

        try:
            photo.thumbnail.delete(save=False)
            photo.image.delete(save=False)
            photo.delete()

            return JsonResponse({
                'success': True,
                'message': "Photo deleted successfully.",
            })

        except (IOError, OSError):
            return JsonResponse({
                'success': False,
                'error': "An unknown error occurred when deleting image files."
            })


def navigate(request, path, method):
    md5 = request.GET.get('md5', '')
    photo = get_photo_by_hash(path, md5)

    try:
        nav = getattr(photo, method)(album=photo.album)
    except Photo.DoesNotExist:
        photos = Photo.objects.filter(album=photo.album)

        # At the oldest photo: return the newest
        if method == 'get_previous_by_taken':
            nav = photos.order_by('-taken')[0]

        # At the newest photo: return the oldest
        elif method == 'get_next_by_taken':
            nav = photos.order_by('taken')[0]

    return photo_to_response(nav)


@api_wrapper
@require_GET
def previous_photo(request, path):
    return navigate(request, path, 'get_previous_by_taken')


@api_wrapper
@require_GET
def next_photo(request, path):
    return navigate(request, path, 'get_next_by_taken')


def navigate_end(path, method):
    album = get_album_by_path(path)
    photos = Photo.objects.filter(album=album).order_by('taken')

    if not photos:
        raise APIError("There are no photos in this album.")

    photo = getattr(photos, method)()

    return photo_to_response(photo)


@api_wrapper
@require_GET
def first_photo(request, path):
    return navigate_end(path, 'first')


@api_wrapper
@require_GET
def last_photo(request, path):
    return navigate_end(path, 'last')


@api_wrapper
@login_required
@require_POST
def upload_photo(request, path):
    files = request.FILES.getlist('files')

    for file in files:
        p = Photo()
        p.album = get_album_by_path(path)

        md5 = generate_md5_hash(file)

        try:
            Photo.objects.get(md5=md5)
        except Photo.DoesNotExist:
            pass
        else:
            raise APIError(f"Duplicate file: {md5}")

        p.md5 = md5
        p.original.save(file.name, file, save=False)

        p.save()

    return JsonResponse({'success': True})


def date_query(start, end):
    query = Q()

    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
        start = start.replace(tzinfo=pytz.utc)
    except ValueError:
        start = False

    try:
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
        end = end.replace(tzinfo=pytz.utc)
    except ValueError:
        end = False

    if start and end:
        query &= Q(taken__gte=start, taken__lte=end)
    elif start or end:
        day = start or end
        day_end = day.replace(hour=23, minute=59, second=59)

        query &= Q(taken__gte=day, taken__lte=day_end)
    else:
        pass

    return query


def search_photos(request):
    params = request.GET
    query = Q(album__hidden=False)

    # Filtering: general

    fields = (
        ('name', 'album__name__icontains', None),
        ('location', 'album__location__icontains', None),
        ('width', 'width', int),
        ('height', 'height', int),
    )

    for key, field, f in fields:
        value = params.get(key, '')

        if value:
            if f is not None:
                value = f(value)

            query &= Q(**{field: value})

    rating = params.getlist('rating')
    if rating:
        subquery = Q()

        for value in rating:
            try:
                value = int(value)
            except ValueError:
                continue

            subquery |= Q(rating=value)

        query = query & subquery

    # Filtering: dates

    taken_start = params.get('taken-start', '')
    taken_end = params.get('taken-end', '')

    uploaded_start = params.get('uploaded-start', '')
    uploaded_end = params.get('uploaded-end', '')

    query &= date_query(taken_start, taken_end)
    query &= date_query(uploaded_start, uploaded_end)

    # Ordering

    order = params.get('order')

    if order not in ('taken', 'edited', 'uploaded'):
        order = 'taken'

    if params.get('direction') == 'new':
        order = f"-{order}"

    # Execute the query!

    photos = Photo.objects.filter(query).order_by(order)
    total = photos.count()

    try:
        page = int(params.get('page'))
    except (ValueError, KeyError):
        page = 1

    # Pagination

    first = ITEMS_PER_PAGE * (page - 1)
    last = first + ITEMS_PER_PAGE

    photos = photos[first:last]

    # Generate the response

    data = [generate_photo_dict(photo, metadata=False, filmstrip=False)
            for photo in photos]

    response = {
        'photos': data,
        'count': total,
    }

    return JsonResponse(response)

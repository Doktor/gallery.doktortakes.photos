import boto3
import botocore.exceptions
import json
import pprint
from invoke import task
from .main import django_setup
from .utils import get_image_file, get_image_filename, get_image_filename_candidate


@task
def rename(ctx, dry_run=False, image_type=None, file='tasks/move_errors.json', print_errors=True):
    """Renames any image files associated with Photo objects."""
    django_setup()
    import photos.models.photo as mp
    from photos.models import Photo

    if dry_run:
        print("Running in 'dry run' mode -- no changes will be made.")

    if image_type not in ['original', 'display_image', 'square_thumbnail', 'thumbnail']:
        print("Invalid image type.")
        raise SystemExit(1)

    with open('data/aws.json') as f:
        data = json.loads(f.read().strip())

    AWS_ACCESS_KEY = data['access']
    AWS_SECRET_KEY = data['secret']
    AWS_BUCKET = data['bucket']

    # Set up S3 connection
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY)
    s3 = session.resource('s3')
    bucket = s3.Bucket(AWS_BUCKET)

    media_prefix = 'media'
    errors = {}

    for photo in Photo.objects.all().iterator():
        image_file = get_image_file(photo, image_type)

        if not image_file:
            print(f"SKIP {photo.pk}")
            continue

        old_name = get_image_filename(photo, image_type)
        new_name = get_image_filename_candidate(photo, image_type)
        assert old_name is not None and new_name is not None

        old_key = media_prefix + '/' + old_name
        new_key = media_prefix + '/' + new_name

        if not old_name:
            print(f"FAIL {old_name}")
            errors[old_name] = {
                'pk': photo.pk,
                'new_name': new_name,
                'error': "missing old name"
            }
            continue

        if old_key == new_key:
            print(f"SKIP {old_name}")
            continue

        if dry_run:
            print(f"TEST {old_name} --> {new_name}")
            continue

        # Copy the file to the new name, preserving public-read permissions
        source = {
            'Bucket': 'doktor',
            'Key': old_key,
        }
        extra_args = {
            'ACL': 'public-read'
        }

        try:
            bucket.copy(source, new_key, extra_args)
        except botocore.exceptions.ClientError as e:
            if '404' in str(e):
                image_field = get_image_file(photo, image_type)
                image_field.name = new_name
                photo.save()

                print(f"FAIL {old_name} 404")
                continue
            else:
                raise RuntimeError("Unknown error") from e

        # Set and save the new filename
        image_field = get_image_file(photo, image_type)
        image_field.name = new_name
        photo.save()

        # Delete the old file
        response = bucket.delete_objects(
            Delete={
                'Objects': [
                    {'Key': old_key},
                ],
            }
        )

        # Final check
        try:
            deleted_key = response['Deleted'][0]['Key']

            if deleted_key != old_key:
                raise RuntimeError
        except (KeyError, RuntimeError) as e:
            errors[old_name] = {
                'pk': photo.pk,
                'new_name': new_name,
                'error': repr(e),
                'exception_type': type(e).__name__,
                'aws_response': response,
            }
            print(f"FAIL {old_name} --> {new_name}")
        else:
            print(f"PASS {old_name} --> {new_name}")

    if dry_run:
        return

    if errors:
        if file:
            with open(file, 'w') as f:
                f.write(json.dumps(errors))

        if print_errors:
            pprint.pprint(errors)

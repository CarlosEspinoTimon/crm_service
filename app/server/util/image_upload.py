import base64
import random
import string

from google.cloud import storage
from flask import current_app


def upload_image(encoded_image, content_type, extension, url=None):
    client = storage.Client(current_app.config['GOOGLE_PROJECT'])
    bucket = client.bucket(current_app.config['GOOGLE_BUCKET'])
    if extension not in ['.jpeg', '.png']:
        raise Exception("Invalid format, image has to be in jpeg or png")
    if url:
        name = url.replace(current_app.config['BUCKET_URL'], '')

    else:
        name = ''.join(random.choices(string.ascii_letters +
                                      string.digits, k=16))

    blob = bucket.blob(name)
    blob.upload_from_string(
        base64.decodebytes(encoded_image.encode()),
        content_type=content_type
    )
    blob.make_public()
    url = blob.public_url

    return url

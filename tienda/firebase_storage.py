"""
Backend de almacenamiento Django para Firebase Storage.
Usa el SDK firebase-admin con Service Account JSON.
"""
import os
import uuid
from datetime import timedelta
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

import firebase_admin
from firebase_admin import credentials, storage as fb_storage


def _init_firebase():
    """Inicializa la app Firebase solo una vez."""
    if not firebase_admin._apps:
        sa_path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_PATH', None)
        bucket = getattr(settings, 'FIREBASE_STORAGE_BUCKET', None)

        if sa_path and os.path.exists(sa_path):
            cred = credentials.Certificate(sa_path)
        else:
            # En producción: credenciales desde variable de entorno JSON
            import json
            sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON', '{}')
            cred = credentials.Certificate(json.loads(sa_json))

        firebase_admin.initialize_app(cred, {'storageBucket': bucket})


@deconstructible
class FirebaseStorage(Storage):
    """Storage backend que guarda archivos en Firebase Storage."""

    def __init__(self, location='media'):
        self.location = location
        _init_firebase()
        self.bucket = fb_storage.bucket()

    def _get_blob_name(self, name):
        return f'{self.location}/{name}'

    def _open(self, name, mode='rb'):
        from django.core.files.base import ContentFile
        blob = self.bucket.blob(self._get_blob_name(name))
        return ContentFile(blob.download_as_bytes())

    def _save(self, name, content):
        # Evitar colisiones de nombre
        ext = os.path.splitext(name)[1]
        unique_name = f'{os.path.splitext(name)[0]}_{uuid.uuid4().hex[:8]}{ext}'
        blob = self.bucket.blob(self._get_blob_name(unique_name))
        content.seek(0)
        blob.upload_from_file(content, content_type=getattr(content, 'content_type', 'application/octet-stream'))
        blob.make_public()
        return unique_name

    def exists(self, name):
        blob = self.bucket.blob(self._get_blob_name(name))
        return blob.exists()

    def url(self, name):
        blob = self.bucket.blob(self._get_blob_name(name))
        if not blob.public_url:
            blob.make_public()
        return blob.public_url

    def size(self, name):
        blob = self.bucket.blob(self._get_blob_name(name))
        blob.reload()
        return blob.size

    def delete(self, name):
        blob = self.bucket.blob(self._get_blob_name(name))
        if blob.exists():
            blob.delete()

    def listdir(self, path):
        blobs = self.bucket.list_blobs(prefix=f'{self.location}/{path}')
        files = [b.name.split('/')[-1] for b in blobs]
        return [], files

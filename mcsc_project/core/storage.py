import logging
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError, BotoCoreError
from django.core.files.storage import FileSystemStorage

logger = logging.getLogger(__name__)

class SupabaseS3Storage(S3Boto3Storage):
    """
    Custom S3Boto3Storage for Supabase S3 API compatibility.
    Outputs clean, static, permanent public URLs directly from Supabase Storage:
    f"{SUPABASE_URL}/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}/{name}"
    """

    def url(self, name, parameters=None, expire=None, http_method=None):
        supabase_url = getattr(settings, 'SUPABASE_URL', '').rstrip('/')
        bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
        if supabase_url and bucket_name:
            clean_name = name.lstrip('/')
            return f"{supabase_url}/storage/v1/object/public/{bucket_name}/{clean_name}"
        return super().url(name, parameters=parameters, expire=expire, http_method=http_method)

    def _save(self, name, content):
        try:
            return super()._save(name, content)
        except (ClientError, BotoCoreError) as err:
            logger.error(f"Supabase S3 upload failed for '{name}': {err}. Falling back to local storage.")
            local_storage = FileSystemStorage()
            return local_storage.save(name, content)

    def exists(self, name):
        try:
            return super().exists(name)
        except ClientError as err:
            status_code = err.response.get('ResponseMetadata', {}).get('HTTPStatusCode')
            if status_code in (403, 404):
                return False
            raise

    def delete(self, name):
        try:
            super().delete(name)
        except ClientError as err:
            status_code = err.response.get('ResponseMetadata', {}).get('HTTPStatusCode')
            if status_code in (403, 404):
                pass  # Ignore missing objects on remote bucket
            else:
                raise


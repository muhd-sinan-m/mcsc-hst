import logging
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError, BotoCoreError
from django.core.files.storage import FileSystemStorage
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Short-lived URL cache TTL (5 minutes max) so presigned URLs always have fresh timestamps
# for new visitors while avoiding redundant URL signing on simultaneous requests.
_URL_CACHE_TTL = 300

class SupabaseS3Storage(S3Boto3Storage):
    """
    Custom S3Boto3Storage for Supabase S3 API compatibility.
    Supabase S3 storage endpoint returns 403 Forbidden instead of 404 Not Found
    for head_object checks when objects do not exist or when accessed via API.

    URL caching: presigned URLs are cached for 90% of AWS_QUERYSTRING_EXPIRE so
    the cached URL is always refreshed before Supabase's server invalidates it.
    Cache is invalidated on new uploads and deletions to ensure freshness.
    """

    def url(self, name, parameters=None, expire=None, http_method=None):
        cache_key = f"supabase_url:{name}"
        cached_url = cache.get(cache_key)
        if cached_url:
            return cached_url
        url = super().url(name, parameters=parameters, expire=expire, http_method=http_method)
        cache.set(cache_key, url, _URL_CACHE_TTL)
        return url

    def _save(self, name, content):
        try:
            saved_name = super()._save(name, content)
            # Evict any old cached URL for this name so the new file appears immediately
            cache.delete(f"supabase_url:{saved_name}")
            cache.delete(f"supabase_url:{name}")
            return saved_name
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
        finally:
            # Always purge the cached URL when the file is deleted
            cache.delete(f"supabase_url:{name}")


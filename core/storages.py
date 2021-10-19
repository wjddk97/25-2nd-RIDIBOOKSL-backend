from ridibooksl.settings       import ( 
    MEDIAFILES_LOCATION, 
    STATICFILES_LOCATION
)
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage) :
    location = MEDIAFILES_LOCATION
    file_overwrite = False

class StaticStorage(S3Boto3Storage) :
    location = STATICFILES_LOCATION
    file_overwrite = False
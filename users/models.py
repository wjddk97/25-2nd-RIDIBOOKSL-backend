from django.db   import models

from core.models import TimeStampModel

class SocialPlatform(TimeStampModel) :
    name = models.CharField(max_length=20)

    class Meta :
        db_table = 'social_platforms'

class User(TimeStampModel) :
    profile_nickname = models.CharField(max_length=40)
    profile_image    = models.CharField(max_length=500, null=True)
    account_email    = models.CharField(max_length=40)
    social_platform  = models.ForeignKey(SocialPlatform, on_delete=models.SET_NULL, null=True)

    class Meta :
        db_table = 'users'
from django.db   import models

from core.models import TimeStampModel

class Subscribe(TimeStampModel) :
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    author = models.ForeignKey('products.Author', on_delete=models.CASCADE)

    class Meta :
        db_table = 'subscribes'
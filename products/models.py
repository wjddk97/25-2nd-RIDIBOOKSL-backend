from django.db   import models

from core.models import TimeStampModel

class Menu(TimeStampModel) :
    name = models.CharField(max_length=20)

    class Meta :
        db_table = 'menus'

class Category(TimeStampModel) :
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    class Meta :
        db_table = 'categories'

class Author(TimeStampModel) :
    name      = models.CharField(max_length=50)
    country   = models.CharField(max_length=20, null=True)
    birthdate = models.DateField(null=True)

    class Meta :
        db_table = 'authors'

class Publisher(TimeStampModel) :
    name = models.CharField(max_length=50)

    class Meta :
        db_table = 'publishers'

class Thumbnail(TimeStampModel) :
    image_url = models.CharField(max_length=500)

    class Meta :
        db_table = 'thumbnails'

class Book(TimeStampModel) :
    menu          = models.ForeignKey(Menu, on_delete=models.CASCADE)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    publisher     = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author        = models.ManyToManyField(Author, through='BookAuthor', related_name='book_author')
    thumbnail     = models.OneToOneField(Thumbnail, on_delete=models.CASCADE)
    main_name     = models.CharField(max_length=100)
    sub_name      = models.CharField(max_length=100, null=True)
    translator    = models.CharField(max_length=20, null=True)
    price         = models.IntegerField()
    trailer       = models.CharField(max_length=600, null=True)
    rent_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    sale_discount = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    class Meta :
        db_table = 'books'

class BookAuthor(TimeStampModel) :
    book   = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta :
        db_table = 'books_authors'

class Rating(TimeStampModel) :
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    book   = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta :
        db_table = 'ratings'

class ViewCount(TimeStampModel) :
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    hit  = models.IntegerField()

    class Meta :
        db_table = 'hits'

class Preview(TimeStampModel) :
    book  = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.CharField(max_length=500)

    class Meta :
        db_table = 'previews'
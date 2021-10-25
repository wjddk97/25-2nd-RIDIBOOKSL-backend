from django.urls    import path

from products.views import *

urlpatterns = [
    path('',ProductView.as_view()),
    path('/search',SearchView.as_view()),
    path('/main',ProductMainView.as_view()),
    path('/<int:book_id>',DetailProductView.as_view()),
    path('/authors/<int:author_id>', AuthorListView.as_view())
]
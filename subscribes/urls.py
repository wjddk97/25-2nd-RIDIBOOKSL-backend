from django.urls import path

from subscribes.views import SubscribeView, SearchView

urlpatterns = [
    path('', SubscribeView.as_view()), 
    path('/search', SearchView.as_view())
]

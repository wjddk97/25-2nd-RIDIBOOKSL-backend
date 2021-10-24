from django.urls import include, path

urlpatterns = [
    path('account', include('users.urls')),
    path('subscribes')
]

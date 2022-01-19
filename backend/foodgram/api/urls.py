from django.urls import include, path

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
# на гет запросы по юзерам нужно будет написать всю хурму: сериализеры, вьюсеты
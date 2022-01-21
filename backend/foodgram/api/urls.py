from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('users', views.UserViewSet)


urlpatterns = [
    # path('users/me/', views.get_me),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]

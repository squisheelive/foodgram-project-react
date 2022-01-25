from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('tags', views.TagViewSet)
router.register('recipes', views.RecipeViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('amounts', views.IngredientAmountViewSet)


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]

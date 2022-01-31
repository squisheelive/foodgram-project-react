from rest_framework import viewsets, mixins
from recipes.models import (Tag, Recipe, Ingredient,
                            Follow, User, Favorite,
                            ShoppingCart)
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (TagSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, IngredientSerializer,
                          SubscribeSerializer, RecipeShortListSerializer)
# from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet as DjoserUserViewSet
from django.conf import settings
from django.http import FileResponse
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(DjoserUserViewSet):

    @action(['get'], detail=False)
    def subscriptions(self, request):

        queryset = [i.following for i in request.user.following.all()]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(
                page,
                many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(
            queryset,
            many=True
            )
        return Response(serializer.data)

    @action(['post', 'delete'], detail=True)
    def subscribe(self, request, id=None):

        current_user = request.user
        user_to_follow = get_object_or_404(User, pk=id)

        if request.method == "DELETE":
            following = get_object_or_404(
                Follow,
                user=current_user,
                following=user_to_follow
            )
            following.delete()
            return Response()

        if current_user == user_to_follow:
            raise ValidationError(
                {'errors': 'Нельзя подписаться на самого себя!'})

        following, status = Follow.objects.get_or_create(
            user=current_user,
            following=user_to_follow
        )

        if status is False:
            raise ValidationError(
                {'errors': 'Вы уже подписаны на этого пользователя!'})

        serializer = SubscribeSerializer(user_to_follow)
        return Response(serializer.data)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipeListSerializer
        else:
            return RecipeCreateSerializer

    # def get_permissions(self):
    #     # надо тут описать пермишн
    #     pass

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )

    @action(['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):

        current_user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite, status = Favorite.objects.get_or_create(user=current_user)
        queryset = favorite.recipes.all()

        if request.method == "DELETE":
            if recipe in queryset:
                recipe.favorite_set.remove(favorite)
                return Response()
            raise ValidationError(
                {'errors': 'Этого рецепта нет в избранном!'})

        if recipe in queryset:
            raise ValidationError(
                {'errors': 'Этот рецепт уже добавлен в избранное!'})

        recipe.favorite_set.add(favorite)
        serializer = RecipeShortListSerializer(recipe)
        return Response(serializer.data)

    @action(['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):

        current_user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        cart, status = ShoppingCart.objects.get_or_create(user=current_user)
        queryset = cart.recipes.all()

        if request.method == "DELETE":
            if recipe in queryset:
                recipe.shoppingcart_set.remove(cart)
                return Response()
            raise ValidationError(
                {'errors': 'Этого рецепта нет в корзине!'})

        if recipe in queryset:
            raise ValidationError(
                {'errors': 'Этот рецепт уже добавлен в корзину!'})

        recipe.shoppingcart_set.add(cart)
        serializer = RecipeShortListSerializer(recipe)
        return Response(serializer.data)

    @action(['get'], detail=False)
    def download_shopping_cart(self, request):

        current_user = request.user
        recipes = Recipe.objects.filter(shoplist__user=current_user)

        if len(recipes) == 0:
            raise ValidationError(
                {'errors': 'Корзина покупок пуста!'})

        ing_amounts = Ingredient.objects.filter(
            recipes__in=recipes).annotate(
                total_amount=Sum('ingredientamount__amount'))

        file_name = f'{current_user.username}.txt'
        file_path = settings.MEDIA_ROOT + '/shopping-carts/' + file_name
        cart_file = open(file_path, 'w+', encoding="utf-8")
        cart_file.write(f'Список покупок пользователя '
                        f'{current_user.username}:\n\n')

        for i in ing_amounts:
            words = len(i.name) + len(i.measurement_unit)
            spacers = ' ' * (50 - words)
            cart_file.write(f'{i.name} ({i.measurement_unit})'
                            f'{spacers}{i.total_amount}\n')
        cart_file.close()

        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
        )

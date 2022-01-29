from rest_framework import viewsets, mixins
from recipes.models import (Tag, Recipe, Ingredient,
                            Follow, User, Favorite)
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (TagSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, IngredientSerializer,
                          SubscribeSerializer, RecipeShortListSerializer)
# from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet as DjoserUserViewSet


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

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipeListSerializer
        else:
            return RecipeCreateSerializer

    def permission_class(self):
        # надо тут описать пермишн
        pass

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )

    @action(['post', 'delete'], detail=True)
    def favorite(self, request, id=None):

        current_user = request.user
        recipe = get_object_or_404(Recipe, pk=id)

        if request.method == "DELETE":
            favorite = get_object_or_404(
                Favorite,
                user=current_user,
                recipe=recipe
            )
            favorite.delete()
            return Response()

        favorite, status = Follow.objects.get_or_create(
            user=current_user,
            recipe=recipe
        )

        if status is False:
            raise ValidationError(
                {'errors': 'Этот рецепт уже добавлен в избранное!'})

        serializer = RecipeShortListSerializer(recipe)
        return Response(serializer.data)
# Написать одну функцию и уноследоваться от нее и к Favorite и к Shopping cart
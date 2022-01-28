from rest_framework import viewsets, mixins
from recipes.models import Tag, Recipe, Ingredient
# from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
from .serializers import (TagSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, IngredientSerializer,
                          SubscribeListSerializer)
# from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet as DjoserUserViewSet


class UserViewSet(DjoserUserViewSet):

    @action(['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):

        queryset = [i.following for i in request.user.following.all()]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeListSerializer(
                page,
                many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeListSerializer(
            queryset,
            many=True
            )
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

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )

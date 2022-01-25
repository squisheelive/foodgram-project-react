from rest_framework import viewsets, mixins
from recipes.models import Tag, Recipe, Ingredient, IngredientAmount
# from rest_framework.serializers import ValidationError
# from rest_framework.decorators import action
# from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (IngredientAmountSerializer, TagSerializer,
                          RecipeListSerializer, IngredientSerializer,
                          RecipeCreateSerializer)
# from rest_framework.permissions import IsAuthenticated


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


class IngredientAmountViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientAmountSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        else:
            return RecipeCreateSerializer

    def perform_create(self, serializer):

        print(self.request.data)
        # ing_list = []
        # for ingredeient_amount in self.request.data['ingredients']:
        #     id = ingredeient_amount['id']
        #     amount = ingredeient_amount['amount']
        #     ingredient = get_object_or_404(Ingredient, pk=id)
        #     ing_amount = IngredientAmount.objects.create(
        #         ingredient=ingredient,
        #         amount=amount
        #     )
        #     ing_list.append(ing_amount)
        # print(ing_list)

        serializer.save(
            author=self.request.user,
        )

from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import (Favorite, Follow, Ingredient, Recipe, ShoppingCart,
                            Tag, User)
from rest_framework import filters, mixins
from rest_framework import status as response_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .filters import RecipeFilter
from .permissions import IsOwnerAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, RecipeShortListSerializer,
                          SubscribeSerializer, TagSerializer)


class UserViewSet(DjoserUserViewSet):

    @action(['get'], detail=False)
    def subscriptions(self, request):

        queryset = User.objects.filter(user__in=request.user.following.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(
                page,
                many=True,
                context={
                    'request': request
                }
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(
            queryset,
            context={
                'request': request
            },
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
            return Response(status=response_status.HTTP_204_NO_CONTENT)

        if current_user == user_to_follow:
            raise ValidationError(
                {'errors': '???????????? ?????????????????????? ???? ???????????? ????????!'}
            )

        following, status = Follow.objects.get_or_create(
            user=current_user,
            following=user_to_follow
        )

        if status is False:
            raise ValidationError(
                {'errors': '???? ?????? ?????????????????? ???? ?????????? ????????????????????????!'}
            )

        serializer = SubscribeSerializer(
            user_to_follow,
            context={
                'request': request
            })
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsOwnerAdminOrReadOnly]

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )

    def favorite_or_shopping_cart(self, request, pk=None, model=None):

        current_user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, status = model.objects.get_or_create(user=current_user)

        if request.method == "DELETE":
            if recipe in obj.recipes.all():
                obj.recipes.remove(recipe)
                serializer = RecipeShortListSerializer(recipe)
                return Response(status=response_status.HTTP_204_NO_CONTENT)
            raise ValidationError(
                {'errors': f'{model._meta.verbose_name} '
                           f'???? ???????????????? ???????? ????????????!'})

        serializer = RecipeShortListSerializer(recipe)

        if recipe not in obj.recipes.all():
            obj.recipes.add(recipe)

        return Response(serializer.data)

    @action(['post', 'delete'], detail=True)
    def favorite(self, request, pk=None, model=Favorite):

        return self.favorite_or_shopping_cart(request=request,
                                              pk=pk,
                                              model=model)

    @action(['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None, model=ShoppingCart):

        return self.favorite_or_shopping_cart(request=request,
                                              pk=pk,
                                              model=model)

    @action(['get'], detail=False)
    def download_shopping_cart(self, request):

        current_user = request.user
        recipes = Recipe.objects.filter(shoplist__user=current_user)

        if len(recipes) == 0:
            raise ValidationError(
                {'errors': '?????????????? ?????????????? ??????????!'})

        ing_amounts = Ingredient.objects.filter(
            recipes__in=recipes).annotate(
                total_amount=Sum('ingredientamount__amount'))

        file_name = f'{current_user.username}.txt'
        file_path = settings.MEDIA_ROOT + file_name
        cart_file = open(file_path, 'w+', encoding="utf-8")
        cart_file.write(f'???????????? ?????????????? ???????????????????????? '
                        f'{current_user.first_name} '
                        f'{current_user.last_name}:\n\n')

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

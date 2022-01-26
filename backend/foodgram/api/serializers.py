from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from recipes.models import (User, Tag, Recipe, Ingredient,
                            Follow, IngredientAmount)
from djoser.serializers import UserCreateSerializer as DjoserCreateSerializer
# from django.shortcuts import get_object_or_404


class UserSerializer(ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if self.context:
            current_user = self.context['request'].user
            if current_user.is_authenticated:
                return Follow.objects.filter(
                    user=current_user,
                    following=obj).exists()
        return False


class UserCreateSerializer(DjoserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountCreateSerializer(ModelSerializer):

    amount = serializers.IntegerField(min_value=1)
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeListSerializer(ModelSerializer):

    tags = TagSerializer(
        many=True
    )
    author = UserSerializer()
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ing_amount'
    )
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:

        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorite(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class RecipeCreateSerializer(ModelSerializer):

    ingredients = IngredientAmountCreateSerializer(
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe, status = Recipe.objects.get_or_create(**validated_data)

        if status is True:

            recipe.tags.set(tags)

            for ing in ingredients:
                ingredient = ing['id']
                amount = ing['amount']
                IngredientAmount.objects.create(
                    ingredient=ingredient,
                    recipe=recipe,
                    amount=amount
                )

        return recipe

    def to_representation(self, value):

        return RecipeListSerializer(value).data

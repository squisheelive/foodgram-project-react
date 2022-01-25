from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from recipes.models import (User, Tag, Recipe, Ingredient,
                            Follow, IngredientAmount)
from djoser.serializers import UserCreateSerializer as DjoserCreateSerializer


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

    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class IngredientAmountCreateSerializer(ModelSerializer):

    id = IngredientSerializer()
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')



class RecipeListSerializer(ModelSerializer):

    tags = TagSerializer(
        many=True,
        source='tag'
    )
    author = UserSerializer()
    ingredients = IngredientAmountSerializer(
        many=True,
        required=True,
        source='ingredient'
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

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tag')    
    image = serializers.SerializerMethodField()
    name = serializers.CharField(
        required=True,
        max_length=200,)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(
        min_value=1,
        max_value=1440
    )

    class Meta:
        model = Recipe
        fields = ('ingredient',
                  'tags',
                  'image',
                  'name',
                  'text',
                  'cooking_time')

    def get_image(self, obj):
        return False

# Валидаторы написать для тэгов и ингредиентов
# 
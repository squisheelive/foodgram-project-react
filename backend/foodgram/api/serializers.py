from rest_framework import serializers
from rest_framework.serializers import ValidationError, ModelSerializer
from recipes.models import (User, Tag, Recipe, Ingredient,
                            Follow, IngredientAmount)


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
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            return Follow.objects.filter(
                user=current_user,
                following=obj)
        return False


class UserCreateSerializer(ModelSerializer):

    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,)
    first_name = serializers.CharField(
        required=True,
        max_length=150,)
    last_name = serializers.CharField(
        required=True,
        max_length=150,)
    password = serializers.CharField(
        required=True,
        max_length=150,)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Такой пользователь уже существует!')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует!')
        return data


class PasswordSerializer(ModelSerializer):

    new_password = serializers.CharField(
        required=True,
        max_length=150,)
    current_password = serializers.CharField(
        required=True,
        max_length=150,)

    class Meta:
        model = User
        fields = ('new_password',
                  'current_password')

    def validate(self, data):
        new_password = data.get('new_password')
        current_password = data.get('current_password')
        if new_password == current_password:
            raise ValidationError('Новый и текущий пароли совпадают!')
        return data


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


class RecipeSerializer(ModelSerializer):

    tag = TagSerializer(many=True, required=True)
    author = UserSerializer(required=True)
    ingredient = IngredientAmountSerializer(many=True, required=True)
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    name = serializers.CharField(
        required=True,
        max_length=200,)
    image = serializers.ImageField()
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(
        min_value=1,
        max_value=1440
    )

    class Meta:
        model = Recipe
        fields = ('__all__')

    def get_is_favorite(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False

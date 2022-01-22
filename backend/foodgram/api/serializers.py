from rest_framework import serializers
from rest_framework.serializers import ValidationError, ModelSerializer
from recipes.models import User, Tag


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

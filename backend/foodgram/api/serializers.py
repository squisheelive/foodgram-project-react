from rest_framework import serializers
from rest_framework.serializers import ValidationError, ModelSerializer
from recipes.models import User


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
        max_length=150,
        allow_blank=False)
    first_name = serializers.CharField(
        required=True,
        max_length=150,
        allow_blank=False)
    last_name = serializers.CharField(
        required=True,
        max_length=150,
        allow_blank=False)
    password = serializers.CharField(
        required=True,
        max_length=150,
        allow_blank=False)

    class Meta:
        model = User
        fields = fields = (
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
            raise ValidationError('Такой пользователь уже существует')
        if username == 'me':  # надо тут на список запрещенных никнеймов отсылать
            raise ValidationError('Данный юзернейм недоступен')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return data

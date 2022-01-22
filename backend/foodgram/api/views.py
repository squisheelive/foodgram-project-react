from rest_framework import viewsets, mixins, status
from recipes.models import User, Tag
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
from .serializers import (UserSerializer, UserCreateSerializer,
                          PasswordSerializer, TagSerializer)
from rest_framework.permissions import IsAuthenticated


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserCreateSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['POST'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']
            print(user.check_password(current_password))

            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

            raise ValidationError('Текущий пароль введен неверно!')
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

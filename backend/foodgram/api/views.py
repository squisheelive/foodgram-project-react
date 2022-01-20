from rest_framework import viewsets, mixins
from recipes.models import User

from .serializers import (UserSerializer, UserCreateSerializer)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserCreateSerializer

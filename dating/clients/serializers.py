from djoser.serializers import UserCreateSerializer
from drf_base64.fields import Base64ImageField

from .models import Client


class CustomImageFiled(Base64ImageField):
    def to_representation(self, value):
        return value.url


class ClientCreateSerializer(UserCreateSerializer):
    avatar = CustomImageFiled(
        error_messages={
            'invalid': 'Не удаётся распознать изображение'
        },
    )

    class Meta:
        model = Client
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'avatar'
        )
        lookup_field = 'username'

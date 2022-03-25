from geopy import distance
from djoser.serializers import UserCreateSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .models import Client, Like


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
            'gender',
            'password',
            'avatar'
        )
        lookup_field = 'username'


class ClientSerializer(serializers.ModelSerializer):
    avatar = CustomImageFiled(
        error_messages={
            'invalid': 'Не удаётся распознать изображение'
        },
    )
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'username',
            'first_name',
            'last_name',
            'gender',
            'avatar',
            'distance',
        )

    def get_distance(self, obj):
        """Return dictance between current user and Client object in km.

        """
        current_user = self.context['request'].user
        point1_coords = (current_user.longitude, current_user.latitude)
        point2_coords = (obj.longitude, obj.latitude)
        return round(distance.distance(point1_coords, point2_coords).km, 2)


class LikeSerializer(serializers.ModelSerializer):
    matcher = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
    )
    matched = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all()
    )
    like = serializers.BooleanField()

    class Meta:
        model = Like
        fields = ('matcher', 'matched', 'like')

    def validate(self, data):
        """
        Check if the user is requested to subscribe on
        is not current user and is not already in subscriptions.
        """
        if data['matcher'] == data['matched']:
            raise serializers.ValidationError(
                'Вы не можете оценивать самого себя.'
            )
        like = Like.objects.filter(
            matcher=data['matcher'],
            matched=data['matched']
        )
        if like.exists():
            raise serializers.ValidationError(
                'Вы уже оценивали этого полльзователя.'
            )
        return data

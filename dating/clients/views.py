import os

from django.conf import settings
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authtoken import views
from rest_framework.permissions import AllowAny

from .serializers import ClientCreateSerializer
from .utilities import ImageEditor


class CreateClientView(APIView):
    """
    View to create clients.
    * Available for all users.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClientCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            avatar_path = serializer.data.get('avatar').lstrip('/')
            full_avatar_path = os.path.join(settings.BASE_DIR, avatar_path)
            editor = ImageEditor(full_avatar_path)
            editor.put_watermark(settings.WATERMARK_PATH)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

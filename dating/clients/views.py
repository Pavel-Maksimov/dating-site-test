import os

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (ClientCreateSerializer, ClientSerializer,
                          LikeSerializer)
from .utilities import ImageEditor, send_emails
from .models import Client, Like


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


class MatchClientView(APIView):
    """View to match other clients.

    If current user sends like=True to a client, check if
    the client have already sent like=True to him (mutual sympathy).
    In this case send back client's email to current user and
    send email massages to them both.
    Available for authenticated users only.
    """
    pemission_classes = [IsAuthenticated]

    def post(self, request, id):
        client = get_object_or_404(Client, id=id)
        data = {
            'matcher': request.user.id,
            'matched': client.id,
            'like': request.data.get('like')
        }
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if request.data.get('like'):
                # проверяем, есть ли положительная оценка с обратной стороны
                reverse_like = Like.objects.filter(
                    matcher=client,
                    matched=request.user,
                    like=True
                )
                if reverse_like.exists:
                    send_emails(client, request.user, settings.EMAIL_NAME)
                    return Response(
                        data={'client_email': client.email},
                        status=status.HTTP_201_CREATED
                    )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ClientsListView(generics.ListAPIView):
    """View to look a list of clients.

    Filtering is available on fields:
    'gender', 'first_name', 'last_name'.
    Available for authenticated users only.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'first_name', 'last_name']

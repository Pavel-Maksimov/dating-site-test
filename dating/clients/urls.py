from multiprocessing.connection import Client
from django.urls import path

from .views import ClientsListView, CreateClientView, MatchClientView


urlpatterns = [
    path('clients/create/', CreateClientView.as_view()),
    path('clients/<int:id>/match/', MatchClientView.as_view()),
    path('list/', ClientsListView.as_view()),
]

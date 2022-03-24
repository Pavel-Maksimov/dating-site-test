from django.urls import path

from .views import CreateClientView


urlpatterns = [
    path('clients/create/', CreateClientView.as_view()),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('list/',ListUser.as_view())
]

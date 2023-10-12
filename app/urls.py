from django.urls import path

from app.view.login_view import LoginAPIView
from app.view.register_view import RegisterApiView

urlpatterns = [

    path("register/", RegisterApiView.as_view(), name='register'),
    path("login/", LoginAPIView.as_view(), name='login'),
]
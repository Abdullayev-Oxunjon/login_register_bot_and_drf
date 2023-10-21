from django.urls import path

from app.view.login_view import LoginAPIView
from app.view.main_view import PersonListCreateAPIView, \
    PersonAPIView, AddGradeView, UpdateGradeView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name='login'),
    path('persons/<int:group_id>/', PersonListCreateAPIView.as_view(), name='persons'),
    path('person/<int:person_id>/', PersonAPIView.as_view(), name='person'),
    path('add-grade/', AddGradeView.as_view(), name='add-grade'),
    path('update-grade/<int:pk>/', UpdateGradeView.as_view(), name='update-grade'),
]

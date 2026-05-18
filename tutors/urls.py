from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutor_list, name='tutor_list'),
    path('<int:pk>/', views.tutor_detail, name='tutor_detail'),
    path('profile/edit/', views.edit_tutor_profile, name='edit_tutor_profile'),
]
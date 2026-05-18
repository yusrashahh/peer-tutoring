from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation'),
    path('start/<int:tutor_id>/', views.start_conversation, name='start'),
    path('<int:conversation_id>/send/', views.send_message, name='send'),
    path('api/unread/', views.unread_count, name='unread_count'),
    path('<int:conversation_id>/poll/', views.poll_messages, name='poll'),
]
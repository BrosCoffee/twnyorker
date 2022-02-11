from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('topic_list', views.topic_list, name='topic_list'),
    path('topic_detail/<str:pk/', views.topic_detail, name='topic_detail'),
    path('topic_create/', views.topic_create, name='topic_create'),
    path('topic_update/<str:pk>/', views.topic_update, name='topic_update'),
    path('topic_delete/<str:pk>/', views.topic_delete, name='topic_delete'),
]
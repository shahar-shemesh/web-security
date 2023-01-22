from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView
from . import views

urlpatterns = [
    #path('', views.home, name='Comunication_LTD-home'),
    path('', PostListView.as_view(), name='Comunication_LTD-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='Comunication_LTD-about'),
]
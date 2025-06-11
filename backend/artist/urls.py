from django.urls import path
from . import views

app_name = 'artist'

urlpatterns = [
    # 게시판 관련
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),    path('post/create/', views.post_create, name='post_create'),
    
    # 아티스트 관련
    path('artists/', views.artist_list, name='artist_list'),
    path('artist/<int:pk>/', views.artist_detail, name='artist_detail'),
    path('artist/<int:artist_pk>/music/add/', views.music_add, name='music_add'),
    
    # 인증 관련
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
]
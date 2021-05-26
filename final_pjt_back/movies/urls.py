from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:movie_pk>/', views.movie_detail, name='detail'),
    path('updatemovie/<int:movie_pk>/', views.movie_update, name='movie_update'),
    path('rankmovie/', views.rankmovie, name='rankmovie'),
    path('review/', views.review_list, name='review_list'),
    path('<int:movie_pk>/review/', views.review_create, name='review_create'),
    path('reviewupdate/<int:review_pk>/', views.review_update, name='review_update'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('findactor/', views.find_actor, name='find_actor'),
    
    
    path('uploadimg/', views.uploadimg, name='uploadimg'),
    path('upload/', views.upload, name='upload'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:movie_pk>/', views.movie_detail, name='detail'),
    path('review/', views.review_list, name='review_list'),
    path('<int:movie_pk>/review/', views.review_create, name='review_create'),
    path('review/<int:review_pk>/', views.review_detail, name='review_detail'),
]

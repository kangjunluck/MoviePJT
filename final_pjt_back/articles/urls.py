from django.urls import path
from . import views


urlpatterns = [
    path('', views.article_list_create),
    path('<int:article_pk>/', views.article_update_delete),
    path('<int:article_pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/', views.comment_list, name='comment_list'),
    path('comment/<int:comment_pk>/', views.comment_update_delete, name='comment_update_delete'),
]

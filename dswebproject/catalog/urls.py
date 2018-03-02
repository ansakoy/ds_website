from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # /catalog/
    path('<int:genre_id>/', views.genre_detail, name='genre_detail'),
]

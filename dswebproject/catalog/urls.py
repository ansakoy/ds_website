from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),  # /catalog/
    # path('<int:genre_id>/', views.genre_detail, name='genre_detail'),
    path('<str:opus_id>/', views.opus_detail, name='opus_detail'),
]

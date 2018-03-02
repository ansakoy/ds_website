from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('<h1>Здесь будет каталог</h1>')


def genre_detail(request, genre_id):
    return HttpResponse("<h2>Detail for genre id: " + str(genre_id) + "</h2>")

from django.shortcuts import render
from django.http import HttpResponse
from .models import Opus

# Create your views here.


# def index(request):
#     return HttpResponse('<h1>Здесь будет каталог</h1>')

def index(request):
    all_works = Opus.objects.all()
    html = ''
    for work in all_works:
        url = '/catalog/' + str(work.id) + '/'
        html += '<a href="' + url + '">' + work.title_ru + ' (' + work.title_am + ')' + '</a><br>'
    return HttpResponse(html)


def genre_detail(request, genre_id):
    return HttpResponse("<h2>Detail for genre id: " + str(genre_id) + "</h2>")


def opus_detail(request, opus_id):
    return HttpResponse("<h2>Detail for genre id: " + str(opus_id) + "</h2>")

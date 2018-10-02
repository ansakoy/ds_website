from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Opus


def index(request):
    all_works = Opus.objects.all()
    context = {'all_works': all_works}
    return render(request, 'catalog/index.html', context)


def genre_detail(request, genre_id):
    return HttpResponse("<h2>Detail for genre id: " + str(genre_id) + "</h2>")


def opus_detail(request, opus_id):
    work = get_object_or_404(Opus, table_pk=opus_id)
    return render(request, 'catalog/detail.html', {'work': work})

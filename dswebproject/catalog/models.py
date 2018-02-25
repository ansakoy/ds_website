from django.db import models

# Create your models here.


class Genre(models.Model):
    name_ru = models.CharField(max_length=250)
    name_am = models.CharField(max_length=250)
    name_en = models.CharField(max_length=250)


class Person(models.Model):
    fname_ru = models.CharField(max_length=250)
    lname_ru = models.CharField(max_length=250)
    fname_am = models.CharField(max_length=250)
    lname_am = models.CharField(max_length=250)
    fname_en = models.CharField(max_length=250)
    lname_en = models.CharField(max_length=250)


class Performer(models.Model):
    performer = models.ManyToManyField(
        Person,
        verbose_name="Автор текста"
    )
    role = models.CharField(max_length=250)


class Performance(models.Model):
    performance_url = models.CharField(max_length=1000)
    title_ru = models.CharField(max_length=500, null=True)
    title_am = models.CharField(max_length=500, null=True)
    title_en = models.CharField(max_length=500, null=True)
    performDate = models.DateField(null=True)
    location = models.CharField(max_length=500, null=True)
    performers = models.ManyToManyField(
        Performer,
        verbose_name="Исполнители")


class Opus(models.Model):
    title_ru = models.CharField(max_length=500)
    title_am = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    comment_ru = models.CharField(max_length=1000)
    comment_am = models.CharField(max_length=1000)
    comment_en = models.CharField(max_length=1000)
    year = models.DateField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        verbose_name="Жанр"
    )
    libretto_by = models.ManyToManyField(
        Person,
        related_name="libr_authors",
        verbose_name="Автор либретто"
    )
    performance = models.ManyToManyField(
        Performance,
        verbose_name="Исполнения"
    )
    lyrics_by = models.ManyToManyField(
        Person,
        related_name="lyr_authors",
        verbose_name="Автор текста"
    )

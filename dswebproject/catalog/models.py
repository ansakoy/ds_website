from django.db import models

# Create your models here.


class Genre(models.Model):
    name_ru = models.CharField(max_length=250, null=True)
    name_am = models.CharField(max_length=250, null=True)
    name_en = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        app_label = 'catalog'


class Person(models.Model):
    fname_ru = models.CharField(max_length=250)
    lname_ru = models.CharField(max_length=250, null=True)
    fname_am = models.CharField(max_length=250, null=True)
    lname_am = models.CharField(max_length=250, null=True)
    fname_en = models.CharField(max_length=250, null=True)
    lname_en = models.CharField(max_length=250, null=True)

    def __str__(self):
        return "%s %s" % (self.fname_ru, self.lname_ru)


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
    table_pk = models.CharField(max_length=10, primary_key=True)
    title_ru = models.CharField(max_length=500)
    title_am = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    comment_ru = models.CharField(max_length=1000)
    comment_am = models.CharField(max_length=1000)
    comment_en = models.CharField(max_length=1000)
    year = models.CharField(max_length=4, null=True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        verbose_name="Жанр",
        null=True
    )
    libretto_by = models.ManyToManyField(
        Person,
        related_name="libr_authors",
        verbose_name="Автор либретто",
    )
    performances = models.ManyToManyField(
        Performance,
        verbose_name="Исполнения",
    )
    lyrics_by = models.ManyToManyField(
        Person,
        related_name="lyr_authors",
        verbose_name="Автор текста",
    )

    def __str__(self):
        return "%s" % self.title_ru

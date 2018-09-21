import os
import django
import csv

os.environ["DJANGO_SETTINGS_MODULE"] = "dswebproject.dsw.settings"


from django.core.wsgi import get_wsgi_application

get_wsgi_application()

django.setup()
from catalog.models import Opus, Person, Genre


def parse_persons(string):
    processed_persons = list()
    if len(string):
        persons = string.split(',')
        for person in persons:
            person = person.strip().split()
            if len(person) == 1:
                fname = person[0].replace('-', ' ')
                lname = None
            else:
                lname = person[-1]
                fname = ' '.join(person[: -1])
            processed_persons.append((fname, lname))
    return processed_persons


def traverse_names(dictionary):
    persons = list()
    dictionary_ru = dictionary['ru']
    if len(dictionary_ru):
        person = dict()
        for idx in range(len(dictionary_ru)):
            person['fname_ru'] = dictionary_ru[idx][0]
            person['lname_ru'] = dictionary_ru[idx][1]
            dictionary_am = dictionary['am']
            if len(dictionary_am):
                try:
                    person['fname_am'] = dictionary_am[idx][0]
                    person['lname_am'] = dictionary_am[idx][1]
                except IndexError:
                    pass
            dictionary_en = dictionary['en']
            if len(dictionary_en):
                try:
                    person['fname_en'] = dictionary_en[idx][0]
                    person['lname_en'] = dictionary_en[idx][1]
                except IndexError:
                    pass
            persons.append(person)
            print(person['fname_ru'], person['lname_ru'])
    return persons


def get_persons_names(row):

    libretto = {'ru': parse_persons(row[3]),
                'am': parse_persons(row[8]),
                'en': parse_persons(row[13])}
    lyrics = {'ru': parse_persons(row[4]),
                'am': parse_persons(row[9]),
                'en': parse_persons(row[14])}

    print(libretto)
    print(lyrics)

    all_persons = traverse_names(libretto)
    if traverse_names(lyrics):
        all_persons += traverse_names(lyrics)
    if len(all_persons):
        for person in all_persons:
            this_person = Person.objects.filter(fname_ru=person['fname_ru'], lname_ru=person['lname_ru'])
            if this_person.count():
                this_person = this_person.first()
                if not this_person.fname_am:
                    this_person.fname_am = person.get('fname_am')
                    this_person.save()
                if not this_person.lname_am:
                    this_person.lname_am = person.get('lname_am')
                    this_person.save()
                if not this_person.fname_en:
                    this_person.fname_en = person.get('fname_en')
                    this_person.save()
                if not this_person.lname_en:
                    this_person.lname_en = person.get('lname_en')
                    this_person.save()
            else:
                this_person = Person(fname_ru=person.get('fname_ru'),
                                     lname_ru=person.get('lname_ru'),
                                     fname_am=person.get('fname_am'),
                                     lname_am=person.get('lname_am'),
                                     fname_en=person.get('fname_en'),
                                     lname_en=person.get('lname_en'))
                this_person.save()


def get_persons_csv(source_file):
    print('INITIAL FOR PERSONS', Person.objects.all().count())
    with open(source_file, 'r', encoding='utf-8') as handler:
        reader = csv.reader(handler)
        count = 0
        for row in reader:
            if count > 0:
                get_persons_names(row)
            count += 1
    print('RESULT FOR PERSONS', Person.objects.all().count())


def get_genre(row):
    results = dict()
    if row:
        if len(row[6]):
            results['ru'] = row[6]  # ru
        if len(row[11]):
            results['am'] = row[11]  # am
        if len(row[16]):
            results['en'] = row[16]  # en
    return results


def insert_genres(results):
    if len(results):
        instance_id = results.get('ru')
        this_genre = Genre.objects.filter(name_ru=instance_id)
        if this_genre.count():
            this_genre = this_genre.first()
            if not this_genre.name_am and results.get('am'):
                this_genre.name_am = results['am']
                this_genre.save()
            if not this_genre.name_en and results.get('en'):
                this_genre.name_en = results['en']
                this_genre.save()
        else:
            this_genre = Genre(name_ru=results['ru'],
                               name_am=results.get('am'),
                               name_en=results.get('en'))
            this_genre.save()


def populate_genre_from_csv(source_file):
    with open(source_file, 'r', encoding='utf-8') as handler:
        reader = csv.reader(handler)
        count = 0
        for row in reader:
            if count > 0:
                genre = get_genre(row)
                insert_genres(genre)
            count += 1
    print('DONE')
    print('ADDED {} GENRES'.format(Genre.objects.all().count()))


def populate_opus(source_file):
    with open(source_file, 'r', encoding='utf-8') as handler:
        reader = csv.reader(handler)
        count = 0
        for row in reader:
            if count > 0:
                opus = Opus()
                opus.table_pk = str(row[0])
                opus.save()
                genre = get_genre(row)
                if len(genre):
                    genre_id = genre.get('ru', '-')
                    genre_entry = Genre.objects.filter(name_ru=genre_id)
                    if genre_entry.count():
                        opus.genre = genre_entry.first()
                libr_by = parse_persons(row[3])
                if len(libr_by):
                    for name in libr_by:
                        person = Person.objects.filter(fname_ru=name[0], lname_ru=name[1])
                        if person.count():
                            opus.libretto_by.add(person.first())
                lyr_by = parse_persons(row[4])
                if len(lyr_by):
                    for name in lyr_by:
                        person = Person.objects.filter(fname_ru=name[0], lname_ru=name[1])
                        if person.count():
                            opus.lyrics_by.add(person.first())
                opus.year = str(row[1])
                opus.title_ru = row[2]
                if len(row[7]):
                    opus.title_am = row[7]
                if len(row[12]):
                    opus.title_en = row[12]
                if len(row[5]):
                    opus.comment_ru = row[5]
                if len(row[10]):
                    opus.comment_am = row[10]
                if len(row[15]):
                    opus.comment_en = row[15]
                opus.save()
            count += 1
    print('DONE')
    print('ADDED {} WORKS'.format(Opus.objects.all().count()))


if __name__ == '__main__':
    # get_persons_csv(r'C:\Users\USER\Documents\PythonProjects\ds_website\Sources\source_catalog_v2.csv')
    # populate_genre_from_csv(r'C:\Users\USER\Documents\PythonProjects\ds_website\Sources\source_catalog_v2.csv')
    populate_opus(r'C:\Users\USER\Documents\PythonProjects\ds_website\Sources\source_catalog_v2.csv')


# o = Opus.objects.all()
#
# for ob in o:
#     print(ob.genre.name_am)
#
# p = Person.objects.all()
# print(p.count())
# for per in p:
#     print(per.lname_ru)
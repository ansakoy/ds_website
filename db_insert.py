import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "dswebproject.dsw.settings"


from django.core.wsgi import get_wsgi_application

get_wsgi_application()

django.setup()
from catalog.models import Opus, Person


o = Opus.objects.all()

for ob in o:
    print(ob.genre.name_am)

p = Person.objects.all()
print(p.count())
for per in p:
    print(per.lname_ru)
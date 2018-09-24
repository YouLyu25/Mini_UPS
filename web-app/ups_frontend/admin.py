from django.contrib import admin
from .models import Person
from .models import package
from .models import item

# Register your models here.
admin.site.register(Person)
admin.site.register(package)
admin.site.register(item)

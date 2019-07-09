from django.contrib import admin
from .models import Person, TestPerson

# Register your models here.
admin.site.register(Person)
admin.site.register(TestPerson)

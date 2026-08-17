from django.contrib import admin
from .models import Course,Scenario,Attempt
admin.site.register([Course,Scenario,Attempt])

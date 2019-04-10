from django.contrib import admin
from cert.models import Person
from cert.models import Certificate
from cert.models import Question
from cert.models import Subject
from cert.models import Assignment

admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Person)
admin.site.register(Assignment)
admin.site.register(Certificate)

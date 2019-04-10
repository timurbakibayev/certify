from django.contrib import admin
from cert.models import Person
from cert.models import TestSet
from cert.models import Test
from cert.models import Certificate
from cert.models import Question
from cert.models import Subject

admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Person)
admin.site.register(TestSet)
admin.site.register(Test)
admin.site.register(Certificate)

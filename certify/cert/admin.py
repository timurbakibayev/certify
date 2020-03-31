from django.contrib import admin
from cert.models import Person
from cert.models import Certificate
from cert.models import Question
from cert.models import Subject
from cert.models import Assignment
from cert.models import AssignedQuestion
from cert.models import QuizStructure
from cert.models import Email


class AdmQuestion(admin.ModelAdmin):
    list_filter = ['subject']
    search_fields = ['question']

admin.site.register(Question, AdmQuestion)
admin.site.register(Subject)
admin.site.register(Person)
admin.site.register(Assignment)
admin.site.register(AssignedQuestion)
admin.site.register(Certificate)
admin.site.register(QuizStructure)
admin.site.register(Email)

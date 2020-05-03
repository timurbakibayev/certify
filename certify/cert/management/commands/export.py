from django.core.management.base import BaseCommand
from cert.models import *
import pandas as pd

class Command(BaseCommand):
    help = 'Runs fake statistics'

    def handle(self, *args, **options):
        print("hello")
        print(len(Question.objects.all()), "questions found")

        _subject_code = []
        _subject_name = []
        _question = []
        _answer1 = []
        _answer2 = []
        _answer3 = []
        _answer4 = []
        _correct_1_to_4 = []

        for question in Question.objects.all():
            _subject_code.append(question.subject.code)
            _subject_name.append(question.subject.name)
            _question.append(question.question)
            _answer1.append(question.answer1)
            _answer2.append(question.answer2)
            _answer3.append(question.answer3)
            _answer4.append(question.answer4)
            _correct_1_to_4.append(question.correct_1_to_4)

        df = pd.DataFrame({
            "subject_code": _subject_code,
            "subject_name": _subject_name,
            "text": _question,
            "answer1": _answer1,
            "answer2": _answer2,
            "answer3": _answer3,
            "answer4": _answer4,
            "correct_1_to_4": _correct_1_to_4,
        } )

        df.to_csv("exported.csv")
        


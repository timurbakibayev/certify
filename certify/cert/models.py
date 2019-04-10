from django.db import models
from django.contrib.auth.models import User

class Certificate(models.Model):
    name = models.CharField(max_length=1000, default="Ivan Pupkin")
    course = models.CharField(max_length=1000, default="Python for Data Science")
    date = models.DateField(default="2019-01-01")
    mark = models.CharField(max_length=1000, default="Excellent")
    permanent_link = models.CharField(max_length=1000, default="AUTO")

    def __str__(self):
        return self.name + " " + self.course


class Subject(models.Model):
    code = models.CharField(max_length=10, default="DS")
    name = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        return f"{self.code}: {self.name}"


class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question = models.TextField(max_length=10000, default="", blank=False, null=False)
    answer1 = models.CharField(max_length=1000, default="", blank=False, null=False)
    answer2 = models.CharField(max_length=1000, default="", blank=False, null=False)
    answer3 = models.CharField(max_length=1000, default="", blank=False, null=False)
    answer4 = models.CharField(max_length=1000, default="", blank=False, null=False)
    correct_1_to_4 = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.subject.code}: {self.question}"


class TestSet(models.Model):
    start_datetime = models.DateTimeField(auto_now_add=True)
    running = models.BooleanField(default=False)


class Person(models.Model):
    last_name = models.CharField(max_length=1000, null=False, blank=False)
    first_name = models.CharField(max_length=1000, null=False, blank=False)
    birth_date = models.DateField(default="2019-01-01")
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING)
    iin = models.CharField(max_length=12, null=False, blank=False)

    def __str__(self):
        return f"{self.last_name} {self.first_name}, ИИН: {self.iin}, Тестов: { Test.objects.filter(person=self) }"


class Test(models.Model):
    name = models.CharField(max_length=1000, null=False, blank=False)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    test_set = models.ForeignKey(TestSet, on_delete=models.DO_NOTHING)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}, running: {self.test_set.running}"

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


class Person(models.Model):
    last_name = models.CharField(max_length=1000, null=False, blank=False)
    first_name = models.CharField(max_length=1000, null=False, blank=False)
    birth_date = models.DateField(default="2019-01-01")
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING)
    iin = models.CharField(max_length=12, null=False, blank=False)

    def __str__(self):
        return f"{self.last_name} {self.first_name}, ИИН: {self.iin}, Тестов: { Assignment.objects.filter(person=self) }"


class QuizStructure(models.Model):
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    subject1 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub1", blank=False, null=False)
    quantity1 = models.IntegerField(default=10)
    subject2 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub2", blank=True, null=True)
    quantity2 = models.IntegerField(default=0)
    subject3 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub3", blank=True, null=True)
    quantity3 = models.IntegerField(default=0)
    subject4 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub4", blank=True, null=True)
    quantity4 = models.IntegerField(default=0)
    subject5 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub5", blank=True, null=True)
    quantity5 = models.IntegerField(default=0)
    subject6 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub6", blank=True, null=True)
    quantity6 = models.IntegerField(default=0)
    subject7 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub7", blank=True, null=True)
    quantity7 = models.IntegerField(default=0)
    subject8 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub8", blank=True, null=True)
    quantity8 = models.IntegerField(default=0)
    subject9 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub9", blank=True, null=True)
    quantity9 = models.IntegerField(default=0)
    subject10 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub10", blank=True, null=True)
    quantity10 = models.IntegerField(default=0)
    subject11 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub11", blank=True, null=True)
    quantity11 = models.IntegerField(default=0)
    subject12 = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="sub12", blank=True, null=True)
    quantity12 = models.IntegerField(default=0)

    def quantity(self):
        to_return = self.quantity1 + self.quantity2 + self.quantity3 + self.quantity4 + self.quantity5 + self.quantity6
        to_return += self.quantity7 + self.quantity8 + self.quantity9 + self.quantity10 + self.quantity11 + self.quantity12
        return to_return

    def __str__(self):
        return f"{self.name}: {self.quantity()} questions"


class Assignment(models.Model):
    assigned_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assgn_by')
    assigned_date_time = models.DateTimeField(auto_now_add=True)
    assigned_code = models.CharField(max_length=100, null=False, blank=False)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assgn_to')
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    score = models.IntegerField(default=0)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    started_date_time = models.DateField(null=True, blank=True)
    finished_date_time = models.DateField(null=True, blank=True)
    total_time = models.IntegerField(default=0)
    certificate = models.ForeignKey(Certificate, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        score = ""
        if self.finished:
            score = f", score: {self.score}"

        return f"{self.person.last_name} {self.person.first_name}, finished: {self.finished}{score}"


class AssignedQuestion(models.Model):
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    answer = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.person.last_name} {self.person.first_name} {self.question}"
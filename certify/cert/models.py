from django.db import models
from django.contrib.auth.models import User


class Email(models.Model):
    domain = models.CharField(max_length=50, default="localhost")
    text = models.TextField(max_length=10000, default="""
Здравствуйте, {{assignment.person.first_name}}! /n
{{assignment.quiz_structure.name}}/n
{{assignment.quiz_structure.minutes}}/n
/n
{{assignment.quiz_structure.quantity}}/n
Логин: {{assignment.person.user.username}}/n
Пароль: {{assignment.person.password}}/n
    """, blank=False, null=False)
    html = models.TextField(max_length=10000, default="""
<html>
<body><p>
Здравствуйте, {{assignment.person.first_name}}!<br>
{{assignment.quiz_structure.name}}<br>
{{assignment.quiz_structure.minutes}}<br>
<br>
{{assignment.quiz_structure.quantity}}<br>
Логин: {{assignment.person.user.username}}<br>
Пароль: {{assignment.person.password}}<br>
</p>
</body>
</hmtl>
        """, blank=False, null=False)
    port = models.IntegerField(default=465)  # For SSL

    sender_email = models.CharField(max_length=50, default="dsacademy.kz@gmail.com")
    subject = models.CharField(max_length=50, default="Тестовая система Data Science Academy")
    smtp_server = models.CharField(max_length=100, default="smtp.gmail.com")
    login = models.CharField(max_length=50, default="dsacademykz@gmail.com")
    password = models.CharField(max_length=50, default="dsadsa5918")

    def __str__(self):
        return f"Domain: {self.domain}"


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
        return f"{self.code}: {self.name}, {len(Question.objects.filter(subject=self))} вопросов"

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question = models.TextField(max_length=10000, default="", blank=False, null=False)
    answer1 = models.CharField(max_length=1000, default="", blank=True, null=True)
    answer2 = models.CharField(max_length=1000, default="", blank=True, null=True)
    answer3 = models.CharField(max_length=1000, default="", blank=True, null=True)
    answer4 = models.CharField(max_length=1000, default="", blank=True, null=True)
    correct_1_to_4 = models.IntegerField(default=1)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.subject.code}: {self.question}"


class Person(models.Model):
    last_name = models.CharField(max_length=1000, null=False, blank=False)
    first_name = models.CharField(max_length=1000, null=False, blank=False)
    birth_date = models.DateField(default="2019-01-01")
    email = models.CharField(max_length=100, default="", blank=True, null=True)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    iin = models.CharField(max_length=12, null=False, blank=False)
    state = models.CharField(max_length=10, default="idle")
    password = models.CharField(max_length=10, default="")

    def __str__(self):
        return f"{self.last_name} {self.first_name}, ИИН: {self.iin}, Тестов: { Assignment.objects.filter(person=self) }"


class SendEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, default="")
    subject = models.CharField(max_length=100, default="")
    text = models.TextField(max_length=10000, default="")
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.email + ": " + ("", "OK")[self.sent]


class QuizStructure(models.Model):
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    minutes = models.IntegerField(default=60)
    regression = models.BooleanField(default=False)
    issue_certificate = models.BooleanField(default=True)
    subject1 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub1", blank=False, null=False)
    quantity1 = models.IntegerField(default=10)
    subject2 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub2", blank=True, null=True)
    quantity2 = models.IntegerField(default=0)
    subject3 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub3", blank=True, null=True)
    quantity3 = models.IntegerField(default=0)
    subject4 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub4", blank=True, null=True)
    quantity4 = models.IntegerField(default=0)
    subject5 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub5", blank=True, null=True)
    quantity5 = models.IntegerField(default=0)
    subject6 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub6", blank=True, null=True)
    quantity6 = models.IntegerField(default=0)
    subject7 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub7", blank=True, null=True)
    quantity7 = models.IntegerField(default=0)
    subject8 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub8", blank=True, null=True)
    quantity8 = models.IntegerField(default=0)
    subject9 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub9", blank=True, null=True)
    quantity9 = models.IntegerField(default=0)
    subject10 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub10", blank=True, null=True)
    quantity10 = models.IntegerField(default=0)
    subject11 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub11", blank=True, null=True)
    quantity11 = models.IntegerField(default=0)
    subject12 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub12", blank=True, null=True)
    quantity12 = models.IntegerField(default=0)

    def quantity(self):
        to_return = self.quantity1 + self.quantity2 + self.quantity3 + self.quantity4 + self.quantity5 + self.quantity6
        to_return += self.quantity7 + self.quantity8 + self.quantity9 + self.quantity10 + self.quantity11 + self.quantity12
        return to_return

    def __str__(self):
        return f"{self.name}: {self.quantity()} questions"


class Assignment(models.Model):
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assgn_by')
    assigned_date_time = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assgn_to')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    quiz_structure = models.ForeignKey(QuizStructure, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    started = models.BooleanField(default=False)
    started_regression = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    finished_regression = models.BooleanField(default=False)
    started_date_time = models.DateTimeField(null=True, blank=True)
    finished_date_time = models.DateTimeField(null=True, blank=True)
    started_regression_date_time = models.DateTimeField(null=True, blank=True)
    finished_regression_date_time = models.DateTimeField(null=True, blank=True)
    coefs = models.CharField(max_length=1000, default="1 1")
    total_time = models.IntegerField(default=0)
    certificate = models.ForeignKey(Certificate, blank=True, null=True, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)
    regression_task = models.CharField(max_length=100, blank=True, null=True)
    regression_solution = models.CharField(max_length=10000, blank=True, null=True)
    regression_tries_left = models.IntegerField(default=5)
    regression_rmse = models.IntegerField(default=-1)
    regression_result = models.IntegerField(default=-1)
    complete = models.BooleanField(default=False)

    def total_score(self):
        if self.quiz_structure.regression:
            return round(self.score_percent()*0.8 + self.regression_result*0.2)
        return round(self.score_percent())

    def score_percent(self):
        if self.quiz_structure.quantity() == 0 or not self.finished:
            return "-"
        return int(self.score / self.quiz_structure.quantity() * 100)

    def __str__(self):
        score = ""
        if self.finished:
            score = f", score: {self.score}"

        return f"{self.person.last_name} {self.person.first_name}, finished: {self.finished}{score}"


class AssignedQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, default="0")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField(default=0)
    answer_text = models.CharField(default='', max_length=1000)
    answered = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.assignment.person.last_name} {self.assignment.person.first_name} {self.question}"

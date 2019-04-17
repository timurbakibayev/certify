from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from cert import adminka
from cert import quiz_flow
from cert.models import Assignment
from cert.email import send_email_from_gmail

latexify = lambda x: x.replace("$","\$")

def log_me_out(request):
    logout(request)
    return redirect("/")


# Create your views here.
def index(request):
    failed_login = False
    print("ddd", request.method)
    if request.method == "POST":
        print("eee", request.POST.get("operation", ""))
        if request.POST.get("operation", "") == "login":
            user = authenticate(username=request.POST.get("username",""), password=request.POST.get("password", ""))
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                failed_login = True

    user = request.user

    if user.is_staff:
        return adminka.index(request)

    if not user.is_authenticated:
        return render(request, "auth.html", {"failed_login": failed_login, "title": adminka.title(request)})

    return quiz_flow.index(request)


def question(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    context = {}

    context["course_name"] = "Yessenov Data Lab Test"
    return render(request, "question.html", context)


def deleteAssignment(request, number):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")
    if not user.is_staff:
        return redirect("/")

    assignment = Assignment.objects.get(pk=number)
    assignment.hidden = True
    assignment.save()


def subject_text(assignment):
    return f"Тестирование: {assignment.quiz_structure.name}"


def body_text(assignment):
    the_text = ""
    the_text += f"Здравствуйте, {assignment.person.first_name}!<br>"
    the_text += f"<br>"
    the_text += f"Добро пожаловать в центр тестирования летней школы YDL!<br>"
    the_text += f"<br>"
    the_text += f"Название теста: {assignment.quiz_structure.name}<br>"
    the_text += f"Длительность: {assignment.quiz_structure.minutes} минут<br>"
    the_text += f"Кол-во вопросов: {assignment.quiz_structure.quantity()}<br>"
    the_text += f"<br>"
    the_text += f"Для начала тестирования зайдите на сайт генерального партнёра летней школы " \
        f"<a href='https://exam.almau.edu.kz'>https://exam.almau.edu.kz</a> " \
        f"и наберите следующие логин и пароль:<br>"
    the_text += f"Логин: {assignment.person.user.username}<br>"
    the_text += f"Пароль: {assignment.person.password}<br>"
    the_text += f"<br>"
    the_text += f"Данный тест необходимо пройти до 21 апреля 2019 г, 23:59. <br>"
    the_text += f"<br>"
    the_text += f"С уважением,<br>"
    the_text += f"Команда научно-образовательного фонда<br>"
    the_text += f"им. академика Ш. Есенова<br>"
    return the_text


def send_email(request, number):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(f"Failed: unathorized")
    if not user.is_staff:
        return HttpResponse(f"Failed: unathorized")
    try:
        assignment = Assignment.objects.get(pk=number)
        send_email_from_gmail(assignment.person.email, subject_text(assignment), body_text(assignment))
        assignment.emailed = True
        assignment.save()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Failed: {e}")

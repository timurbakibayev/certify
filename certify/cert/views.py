from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from cert import adminka
from cert import quiz_flow
from cert.models import Assignment

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

    context = {
        "question": latexify("Что такое $x^2$ Data Science?"), "answer1": latexify("d$\\frac{1}{2}$"), "answer2": "Раковина", "answer3": "Зеркало",
                "answer4": "Вода", "correct": 4}

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

def sendEmail(request, number):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")
    if not user.is_staff:
        return redirect("/")
    assignment = Assignment.objects.get(pk=number)
    assignment.save()

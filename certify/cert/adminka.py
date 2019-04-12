from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from cert.models import Assignment
from cert.models import QuizStructure
from cert.models import Person
import random
import string


def title(request):
    title = ""
    print("uri",request.build_absolute_uri())
    if "almau" in request.build_absolute_uri():
        title = "AlmaU"
    if "dsacademy" in request.build_absolute_uri():
        title = "Data Science Academy"
    if "localhost" in request.build_absolute_uri():
        title = "localhost"

    return title

def index(request):
    user = request.user
    if request.method == "POST":
        try:
            quiz = QuizStructure.objects.get(pk=int(request.POST.get("quiz")))
            iin = request.POST.get("iin")
            last_name = request.POST.get("last_name")
            first_name = request.POST.get("first_name")
            if len(iin) > 0:
                same_persons = Person.objects.filter(iin=iin)
                if len(same_persons) > 0:
                    person = same_persons[0]
                else:
                    new_user = User()
                    new_user.username = iin
                    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    new_user.set_password(password)
                    new_user.save()
                    person = Person()
                    person.iin = iin
                    person.first_name = first_name
                    person.last_name = last_name
                    person.user = new_user
                    person.password = password
                    person.save()
                ass = Assignment()
                ass.person = person
                ass.quiz_structure = quiz
                ass.assigned_by = user
                ass.assigned_to = person.user
                ass.save()
                return redirect("/")
        except Exception as e:
            return redirect("/")

    context = {}
    assignments = Assignment.objects.filter(assigned_by=user)
    quizes = QuizStructure.objects.all()

    if len(assignments) > 0:
        ass = assignments[len(assignments)-1]
        context["default_value"] = ass.quiz_structure.id
        context["default_text"] = ass.quiz_structure.name
    elif len(quizes) > 0:
        quiz = quizes[0]
        context["default_value"] = quiz.id
        context["default_text"] = quiz.name


    context["assignments"] = assignments
    context["quiz_structures"] = quizes
    context["title"] = title(request)

    return render(request, "adminka.html", context=context)
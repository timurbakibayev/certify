from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from cert.models import Assignment
from cert.models import AssignedQuestion
from cert.models import QuizStructure
from cert.models import Question
from cert.models import Person


def index(request):
    user = request.user
    person = Person.objects.get(user=user)
    assignments = Assignment.objects.filter(hidden=False).filter(person=person).filter(complete=True)

    return render(request,"certificates.html",{"assignments":assignments})
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from cert.models import Assignment
from cert.models import AssignedQuestion
from cert.models import QuizStructure
from cert.models import Question
from cert.models import Person
import random
import string
from cert.adminka import title
import datetime
from pytz import timezone
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os.path import join
from certify import settings


def regression_start(request):
    user = request.user
    person = Person.objects.get(user=user)
    check = Assignment.objects.filter(person=person).filter(hidden=False).filter(finished=True).filter(started_regression=True).filter(finished_regression=False)
    if len(check) > 0:
        return HttpResponse("Already has an open regression assignment")
    try:
        ass = Assignment.objects.filter(person=person).filter(hidden=False).filter(finished=True).filter(started_regression=False)[0]
        ass.started_regression = True
        ass.started_regression_date_time = datetime.datetime.now()
        ass.regression_task = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        ass.save()

        df = pd.DataFrame({
            "x1": np.random.randint(300, size=120),
            "x2": np.random.randint(150, size=120),
            "x3": np.random.randint(100, size=120),
            "x4": np.random.randint(10, size=120),
            "x5": np.random.randint(200, size=120),
        })

        df["f"] = random.randint(0,4) * (df["x1"] ** random.randint(0, 2))
        df["f"] = df["f"] + random.randint(0,4) * (df["x2"] ** random.randint(0, 2))
        df["f"] = df["f"] + random.randint(0,4) * (df["x3"] ** random.randint(0, 2))
        df["f"] = df["f"] + random.randint(0,4) * (df["x4"] ** random.randint(0, 2))
        df["f"] = df["f"] + random.randint(0,4) * (df["x5"] ** random.randint(0, 2))
        df["f"] = df["f"] + (np.random.randint(50, size=120) - 25)

        df1 = df[:100]
        df2 = df[100:]
        df3 = df[100:].drop(["f"],axis=1)

        df1.to_csv(join(settings.MEDIA_ROOT, f"{ass.regression_task}_train.csv"), index=False)
        df3.to_csv(join(settings.MEDIA_ROOT, f"{ass.regression_task}_test.csv"), index=False)

        ass.regression_solution = ",".join([str(i) for i in df2["f"].tolist()])
        ass.save()

        return HttpResponse("OK")
    except Exception as e:
        print(str(e))
        return HttpResponse("Oops, something went wrong")


def show_question(request, ass):
    error_text = ""

    current_error = -1
    show_current_error = False

    if request.method == "POST":
        answer = request.POST.get("answer", "")
        if len(answer.split(",")) != 20:
            error_text = "Необходимо ввести 20 чисел, разделенных запятой!"
        elif ass.regression_tries_left <= 0:
            error_text = "Превышено количество попыток"
        else:
            try:
                answers = [float(i.strip()) for i in answer.split(",")]
                correct_answers = [int(i.strip()) for i in ass.regression_solution.split(",")]
                percent_loss = [(correct_answers[i] - answers[i])/correct_answers[i]*100 for i in range(len(answers))]
                current_error = abs(int(sum(percent_loss)/len(correct_answers) * 100)/100)
                show_current_error = True
                if ass.regression_rmse == -1 or ass.regression_rmse > current_error:
                    ass.regression_rmse = current_error
                ass.regression_tries_left -= 1
                ass.save()
            except:
                error_text = "Неверный формат ввода данных"

    if ass.regression_rmse >= 0:
        error = ass.regression_rmse
    else:
        error = -1

    context = {"ass": ass,
               "error_text": error_text,
               "current_error": current_error,
               "show_current_error": show_current_error,
               "error": error,
               }

    return render(request, "question_reg.html", context=context)


def finish_regression(request):
    user = request.user
    person = Person.objects.get(user=user)
    ass = Assignment.objects.filter(person=person).filter(hidden=False)[len(Assignment.objects.filter(hidden=False).filter(person=person)) - 1]
    if not ass.finished_regression:
        ass.finished_regression = True
        ass.regression_result = 100 - ass.regression_rmse
        if ass.regression_rmse < 0:
            ass.regression_result = 0
        ass.finished_regression_date_time = datetime.datetime.now()
        ass.save()
    return HttpResponse("OK")

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
from cert import regression
from cert import certificates

latexify = lambda x: x.replace("$","\$")


def index(request):
    user = request.user
    person = Person.objects.get(user=user)

    try:
        ass = Assignment.objects.filter(hidden=False).filter(person=person).filter(finished=False)[0]
    except:
        ass = Assignment.objects.filter(hidden=False).filter(person=person)[len(Assignment.objects.filter(hidden=False).filter(person=person))-1]
        if ass.complete:
            return certificates.index(request)
        questions_total = len(AssignedQuestion.objects.filter(assignment=ass))
        context = {"person": person, "assignment": ass,
                   "questions_total": questions_total,
                   }
        if not ass.started_regression:
            return render(request, "results.html", context)
        elif ass.finished_regression:
            return render(request, "results_with_regression.html", context)
        else:
            return regression.show_question(request, ass)

    print("Current Assignment:", ass.id)
    context = {"person": person, "assignment": ass}

    if not ass.started:
        return render(request, "quiz_start.html", context)

    if time_left(request) == 0:
        questions = AssignedQuestion.objects.filter(assignment=ass).filter(answered=False)
        for qu in questions:
            qu.answered = True
            qu.correct = False
            qu.save()

    try:
        question = AssignedQuestion.objects.filter(assignment=ass).filter(answered=False)[0].question
        ass.current_question = question
        ass.save()
    except:
        ass.finished = True
        ass.finished_date_time = datetime.datetime.now()
        ass.score = len(AssignedQuestion.objects.filter(assignment=ass).filter(correct=True))
        ass.save()
        return redirect("/")

    question_number = len(AssignedQuestion.objects.filter(assignment=ass).filter(answered=False))
    questions_total = len(AssignedQuestion.objects.filter(assignment=ass))
    question_number = questions_total - question_number + 1

    context = {"person": person, "assignment": ass, "question": ass.current_question,
               "question_text": latexify(ass.current_question.question),
               "answer1": latexify(ass.current_question.answer1),
               "answer2": latexify(ass.current_question.answer2),
               "answer3": latexify(ass.current_question.answer3),
               "answer4": latexify(ass.current_question.answer4),
               "question_number": question_number,
               "questions_total": questions_total,
               "question_lines": [
                   {"text": latexify(i), "padding": str((len(i) - len(i.lstrip())) / 2)} for i in
                   ass.current_question.question.split("\n")
               ]
               }

    if ass.finished:
        render(request, "results.html", context)

    return render(request, "question.html", context)
    # except:
    #     return render(request, "daswares.html", context)


def reply(request, number):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")
    try:
        person = Person.objects.get(user=user)
        ass = Assignment.objects.filter(hidden=False).filter(person=person).filter(finished=False)[0]
        assigned_question = AssignedQuestion.objects.filter(assignment=ass).filter(answered=False)[0]
        assigned_question.answered = True
        assigned_question.answer = number
        assigned_question.correct = number == assigned_question.question.correct_1_to_4
        assigned_question.save()
        return HttpResponse("OK")
    except Exception as e:
        print(str(e))
        return HttpResponse("FAIL")


def start(request):
    """
    :param request:
    :return: Starting the quiz, shuffling the questions, assignment
    """
    user = request.user
    if not user.is_authenticated:
        return redirect("/")
    person = Person.objects.get(user=user)
    if len(Assignment.objects.filter(hidden=False).filter(person=person).filter(started=True).filter(finished=False)) > 0:
        return HttpResponse("Already started")
    if len(Assignment.objects.filter(hidden=False).filter(person=person).filter(started=False)) == 0:
        return HttpResponse("No test to start")
    ass = Assignment.objects.filter(hidden=False).filter(person=person).filter(started=False)[0]
    qs = ass.quiz_structure
    qs_list = [
        {"subject": qs.subject1, "quantity": qs.quantity1},
        {"subject": qs.subject2, "quantity": qs.quantity2},
        {"subject": qs.subject3, "quantity": qs.quantity3},
        {"subject": qs.subject4, "quantity": qs.quantity4},
        {"subject": qs.subject5, "quantity": qs.quantity5},
        {"subject": qs.subject6, "quantity": qs.quantity6},
        {"subject": qs.subject7, "quantity": qs.quantity7},
        {"subject": qs.subject8, "quantity": qs.quantity8},
        {"subject": qs.subject9, "quantity": qs.quantity9},
        {"subject": qs.subject10, "quantity": qs.quantity10},
        {"subject": qs.subject11, "quantity": qs.quantity11},
        {"subject": qs.subject12, "quantity": qs.quantity12},
    ]
    for qs_item in qs_list:
        if qs_item["quantity"] > 0:
            print(qs_item["subject"], qs_item["quantity"])
            subject = qs_item["subject"]
            quantity = qs_item["quantity"]
            all_questions = [i.id for i in Question.objects.filter(subject=subject)]
            random.shuffle(all_questions)
            if len(all_questions) > 0:
                while len(all_questions) < quantity:
                    all_questions += all_questions
            for q_id in all_questions[:quantity]:
                question = Question.objects.get(pk=q_id)
                assigned = AssignedQuestion()
                assigned.person = person
                assigned.question = question
                assigned.assignment = ass
                assigned.save()

    ass.started = True
    ass.started_date_time = datetime.datetime.now()
    ass.save()

    return HttpResponse("OK")


def time_left(request):
    try:
        person = Person.objects.filter(user=request.user)[0]
        ass = Assignment.objects.filter(hidden=False).filter(person=person).filter(started=True).filter(finished=False)[0]
        timedelta = datetime.datetime.now(timezone("Asia/Almaty")) - ass.started_date_time
        if ass.quiz_structure.minutes * 60 - timedelta.seconds <= 0:
            return 0
        timedelta = ass.quiz_structure.minutes * 60 - timedelta.seconds
        return timedelta
    except Exception as e:
        return -1


def time_left_http(request):
    if time_left(request) // 60 // 60 > 0:
        human = f"{time_left(request) // 60 // 60} ч {time_left(request) // 60 % 60} м"
    elif time_left(request) // 60 == 0:
        human = f"{time_left(request) % 60} с"
    else:
        human = f"{time_left(request) // 60} м"

    return HttpResponse(human)


def test_question(request, number):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect("/")
    question = Question.objects.get(pk=number)
    context = {"question": question,
               "question_text": latexify(question.question),
               "answer1": latexify(question.answer1),
               "answer2": latexify(question.answer2),
               "answer3": latexify(question.answer3),
               "answer4": latexify(question.answer4),
               "question_number": 1,
               "questions_total": 10,
               "question_lines": [
                   {"text":latexify(i), "padding":str((len(i)-len(i.lstrip()))/2)} for i in question.question.split("\n")
               ]
               }

    return render(request, "question.html", context)


def test_results(request, number):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect("/")
    ass = Assignment.objects.get(pk=number)
    questions_total = len(AssignedQuestion.objects.filter(assignment=ass))

    qs = ass.quiz_structure
    qs_list = [
        {"subject": qs.subject1, "quantity": qs.quantity1},
        {"subject": qs.subject2, "quantity": qs.quantity2},
        {"subject": qs.subject3, "quantity": qs.quantity3},
        {"subject": qs.subject4, "quantity": qs.quantity4},
        {"subject": qs.subject5, "quantity": qs.quantity5},
        {"subject": qs.subject6, "quantity": qs.quantity6},
        {"subject": qs.subject7, "quantity": qs.quantity7},
        {"subject": qs.subject8, "quantity": qs.quantity8},
        {"subject": qs.subject9, "quantity": qs.quantity9},
        {"subject": qs.subject10, "quantity": qs.quantity10},
        {"subject": qs.subject11, "quantity": qs.quantity11},
        {"subject": qs.subject12, "quantity": qs.quantity12},
    ]
    subjects = []
    for qs_item in qs_list:
        if qs_item["quantity"] > 0:
            subject = qs_item["subject"]
            assignments = AssignedQuestion.objects.filter(assignment=ass).filter(question__subject=subject)
            subjects.append({
                "name": subject.name,
                "quantity": len(assignments),
                "correct": len(assignments.filter(correct=True)),
                "percent": int(len(assignments.filter(correct=True))/len(assignments)*100),
            })


    context = {"person": ass.person, "assignment": ass,
               "questions_total": questions_total,
               "subjects": subjects,
               }

    return render(request, "results_detailed.html", context)

def questions_list(request, number):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect("/")

    ass = Assignment.objects.get(pk=number)
    questions = AssignedQuestion.objects.filter(assignment=ass)

    context = {"person": ass.person, "assignment": ass,
               "questions": questions,
               }

    return render(request, "questions_list.html", context)

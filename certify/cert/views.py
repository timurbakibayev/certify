from django.shortcuts import render


latexify = lambda x: x.replace("$","\$")

# Create your views here.
def index(request):
    context = {}
    return render(request, "index.html", context)


def question(request):
    context = {
        "question": latexify("Что такое $x^2$ Data Science?"), "answer1": latexify("d$\\frac{1}{2}$"), "answer2": "Раковина", "answer3": "Зеркало",
                "answer4": "Вода", "correct": 4}

    context["course_name"] = "Yessenov Data Lab Test"
    return render(request, "question.html", context)

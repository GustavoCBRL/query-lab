from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import User, Topics, Questions, Choices, UserAnswer, PracticeExercise, PracticeSubmission
import sqlite3
import json


# Create your views here.


def paginate_posts(request, topics):
    paginator = Paginator(topics, 10)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def index(request):
    topics = Topics.objects.order_by("id")
    questions = Questions.objects.all()
    page_obj = paginate_posts(request, topics)

    return render(request, "study_hub/index.html", {
        "topics": page_obj,
        "questions": questions
    })



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "study_hub/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "study_hub/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "study_hub/register.html")
    
@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topics, pk=topic_id)
    return JsonResponse({
        "id": topic.id,
        "title": topic.title,
        "summary": topic.summary,
        "theory": topic.theory,
        "questions": [
            {
                "id": question.id,
                "statement": question.statement,
                "explanation": question.explanation,
                "choices":[
                    {
                        "id": choice.id,
                        "text": choice.text 
                    }
                    for choice in question.choice.all()
                ]
            }
            for question in topic.questions.all()
        ]
    })


@login_required
def submit_answer(request, question_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required!"},
            status=400
        )

    question_id = request.POST.get("question_id")
    choice_id = request.POST.get("choice_id")
    question = get_object_or_404(Questions, pk=question_id)
    choice = get_object_or_404(Choices, pk=choice_id)




    if UserAnswer.objects.filter(user=request.user, question=question).exists():
        return JsonResponse(
            {"error": "You have already answered this question."},
            status=409
        )        


    UserAnswer.objects.create(
        user=request.user,
        question=question,
        selected_choice=choice,
        is_correct=choice.is_correct
    )

    return JsonResponse({
        "correct": choice.is_correct,
        "explanation": question.explanation
    })

@login_required
def dashboard(request):

    answered_count = UserAnswer.objects.filter( user = request.user ).count()
    correct_count = UserAnswer.objects.filter(user = request.user, is_correct=True).count()
    total_questions = Questions.objects.count()

    accuracy = 0
    progress = 0

    if answered_count:
        accuracy = round(correct_count/answered_count * 100, 1)

    if total_questions:
        progress = round(answered_count/ total_questions * 100, 1)

    topics_progress = []

    for topic in Topics.objects.all():
        total_topic = topic.questions.count()
        correct_topic_count = UserAnswer.objects.filter(user=request.user, is_correct=True, question__topic=topic).count()
        answered_topic_count = UserAnswer.objects.filter(user=request.user, question__topic=topic).count()
        progress_topic = 0
        accuracy_topic = 0

        if total_topic:
            progress_topic = round(answered_topic_count / total_topic * 100, 1)

        if answered_topic_count:
            accuracy_topic = round(correct_topic_count / answered_topic_count * 100, 1)

        topics_progress.append({
            "title": topic.title,
            "progress_topic": progress_topic,
            "accuracy_topic": accuracy_topic
        })

    best_topic = max(topics_progress, key=lambda x: x["accuracy_topic"]) if topics_progress else {"title": "N/A"}

    return render(
        request,
        "study_hub/dashboard.html", {
            "accuracy": accuracy,
            "progress": progress,
            "topics_progress": topics_progress,
            "correct_count": correct_count,
            "answered_count": answered_count,
            "best_topic": best_topic
        }
    )

@login_required
def practice_list(request, topic_id=None):
    topic = None

    if topic_id is not None:
        topic = get_object_or_404(Topics, pk=topic_id)
        practices = topic.practices.all()
        completed_ids = set(
            PracticeSubmission.objects.filter(
                user=request.user,
                practice__topic=topic,
                is_correct=True
            ).values_list("practice_id", flat=True)
        )
    else:
        practices = PracticeExercise.objects.select_related("topic").all()
        completed_ids = set(
            PracticeSubmission.objects.filter(
                user=request.user,
                is_correct=True
            ).values_list("practice_id", flat=True)
        )

    for practice in practices:
        practice.completed = practice.id in completed_ids

    return render(
        request,
        "study_hub/practice_list.html",
        {
            "topic": topic,
            "practices": practices
        }
    )



@login_required
def practice_exercise(request, practice_id):

    practice = get_object_or_404(PracticeExercise,pk=practice_id)
    context = {
        "practice": practice
    }

    if request.method == "POST":
        submitted_query = request.POST.get(
            "query",
            ""
        )

        expected_conn = None
        user_conn = None

        try:
            expected_conn, expected_cursor = build_practice_db(practice.dataset)
            user_conn, user_cursor = build_practice_db(practice.dataset)

            expected_cursor.execute(practice.expected_query)
            expected_result = expected_cursor.fetchall()

            user_cursor.execute(submitted_query)
            user_result = user_cursor.fetchall()
            
            is_correct = user_result == expected_result

            PracticeSubmission.objects.create(
                user=request.user,
                practice=practice,
                submitted_query=submitted_query,
                is_correct=is_correct
            )

            context.update({
                "submitted_query": submitted_query,
                "user_result": user_result,
                "expected_result": expected_result,
                "is_correct": is_correct
            })
        except Exception as error:
            context.update({
                "submitted_query": submitted_query,
                "error": str(error)
            })
        finally:
            if expected_conn is not None:
                expected_conn.close()
            if user_conn is not None:
                user_conn.close()
    return render(
        request,
        "study_hub/practice.html",
        context
    )

def build_practice_db(dataset):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    for table_name, rows in dataset.items():
        if not rows:
            continue

        first_row = rows[0]
        columns = [f"{column} TEXT" for column in first_row.keys()]

        cursor.execute(
            f'''
            CREATE TABLE {table_name} (
                {",".join(columns)}
            )
            '''
        )

        for row in rows:
            row_columns = list(row.keys())
            values = list(row.values())
            placeholders = ",".join(["?"] * len(values))

            cursor.execute(
                f'''
                INSERT INTO {table_name}
                ({",".join(row_columns)})
                VALUES ({placeholders})
                ''',
                values,
            )

    return conn, cursor

    


        


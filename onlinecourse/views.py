from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Course, Lesson, Question, Choice, Enrollment, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, "onlinecourse/course_list.html", {"courses": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course, "lessons": course.lessons.all()},
    )


@login_required
def mock_exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.prefetch_related("choices").all()
    return render(
        request,
        "onlinecourse/mock_exam.html",
        {"course": course, "questions": questions},
    )


@login_required
def submit(request, course_id):
    if request.method != "POST":
        return redirect("mock_exam", course_id=course_id)

    course = get_object_or_404(Course, pk=course_id)
    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={"mode": Enrollment.AUDIT},
    )

    submission = Submission.objects.create(enrollment=enrollment)
    score = 0.0

    for question in course.questions.prefetch_related("choices").all():
        selected_ids = request.POST.getlist(f"question_{question.pk}")
        selected_choices = list(
            Choice.objects.filter(
                question=question,
                pk__in=selected_ids,
            )
        )
        submission.choices.add(*selected_choices)

        correct_ids = set(
            question.choices.filter(is_correct=True).values_list("id", flat=True)
        )
        selected_set = {choice.pk for choice in selected_choices}

        if correct_ids and selected_set == correct_ids:
            score += question.grade

    submission.total_score = score
    submission.save()

    return redirect("show_exam_result", submission_id=submission.pk)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("enrollment__course"),
        pk=submission_id,
        enrollment__user=request.user,
    )
    course = submission.enrollment.course
    questions = course.questions.prefetch_related("choices").all()
    results = []

    for question in questions:
        correct_choices = question.choices.filter(is_correct=True)
        selected_choices = submission.choices.filter(question=question)
        correct_ids = set(correct_choices.values_list("id", flat=True))
        selected_ids = set(selected_choices.values_list("id", flat=True))
        results.append({
            "question": question,
            "selected_choices": selected_choices,
            "correct_choices": correct_choices,
            "is_correct": bool(correct_ids) and selected_ids == correct_ids,
        })

    max_score = sum(q.grade for q in questions)
    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "submission": submission,
            "course": course,
            "results": results,
            "max_score": max_score,
        },
    )

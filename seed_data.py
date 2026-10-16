from django.contrib.auth import get_user_model
from django.utils import timezone
from onlinecourse.models import Course, Lesson, Question, Choice

User = get_user_model()

# Create a real local demo account for testing the exam.
student, created = User.objects.get_or_create(
    username="demo_student",
    defaults={"email": "demo_student@example.com"},
)
if created:
    student.set_password("DemoStudent2026!")
    student.save()

# Create sample course.
course, _ = Course.objects.get_or_create(
    name="Python Fundamentals",
    defaults={
        "description": "Learn Python basics, variables, data types, and functions.",
        "pub_date": timezone.localdate(),
    },
)

# Create lessons.
Lesson.objects.get_or_create(
    course=course, order=1,
    defaults={
        "title": "Introduction to Python",
        "content": "Python is a programming language used for web development, automation, and data science.",
    },
)
Lesson.objects.get_or_create(
    course=course, order=2,
    defaults={
        "title": "Variables and Data Types",
        "content": "Variables store values. Common Python types include integers, strings, floats, and booleans.",
    },
)

# Create two questions with genuine answer keys.
q1, _ = Question.objects.get_or_create(
    course=course,
    question_text="Which keyword defines a function in Python?",
    defaults={"grade": 1.0},
)
Choice.objects.get_or_create(
    question=q1, choice_text="def",
    defaults={"is_correct": True},
)
Choice.objects.get_or_create(
    question=q1, choice_text="function",
    defaults={"is_correct": False},
)
Choice.objects.get_or_create(
    question=q1, choice_text="func",
    defaults={"is_correct": False},
)

q2, _ = Question.objects.get_or_create(
    course=course,
    question_text="Which data type represents True or False?",
    defaults={"grade": 1.0},
)
Choice.objects.get_or_create(
    question=q2, choice_text="Boolean",
    defaults={"is_correct": True},
)
Choice.objects.get_or_create(
    question=q2, choice_text="String",
    defaults={"is_correct": False},
)
Choice.objects.get_or_create(
    question=q2, choice_text="List",
    defaults={"is_correct": False},
)

print("Sample data ready.")
print("Course:", course.name, "| ID:", course.pk)
print("Lessons:", course.lessons.count())
print("Questions:", course.questions.count())
print("Demo account:", student.username)

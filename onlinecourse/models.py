from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    STUDENT = "STUDENT"
    DEVELOPER = "DEVELOPER"
    DATA_SCIENTIST = "DATA_SCIENTIST"
    DATABASE_ADMIN = "DATABASE_ADMIN"

    OCCUPATION_CHOICES = [
        (STUDENT, "Student"),
        (DEVELOPER, "Developer"),
        (DATA_SCIENTIST, "Data Scientist"),
        (DATABASE_ADMIN, "Database Admin"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT)
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=100, default="Online Course")
    image = models.ImageField(upload_to="course_images/", blank=True)
    description = models.TextField()
    pub_date = models.DateField(null=True, blank=True)
    instructors = models.ManyToManyField(Instructor, blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Enrollment",
        related_name="enrolled_courses",
    )
    total_enrollment = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Lesson")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    content = models.TextField()

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    AUDIT = "AUDIT"
    HONOR = "HONOR"
    BETA = "BETA"
    COURSE_MODES = [(AUDIT, "Audit"), (HONOR, "Honor"), (BETA, "Beta")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return f"{self.user} - {self.course}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=250)
    grade = models.FloatField(default=1.0)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        correct_ids = set(self.choices.filter(is_correct=True).values_list("id", flat=True))
        return bool(correct_ids) and correct_ids.issubset(set(selected_ids))


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="submissions")
    choices = models.ManyToManyField(Choice, blank=True)
    total_score = models.FloatField(default=0.0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission #{self.pk} - {self.total_score}"

from django.urls import path
from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("courses/<int:course_id>/", views.course_details, name="course_details"),
    path("courses/<int:course_id>/exam/", views.mock_exam, name="mock_exam"),
    path("courses/<int:course_id>/submit/", views.submit, name="submit"),
    path("results/<int:submission_id>/", views.show_exam_result, name="show_exam_result"),
]

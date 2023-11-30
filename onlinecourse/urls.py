from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    LessonListView,
    LessonDetailView,
    QuestionListView,
    enroll,
    submit,
    show_exam_result
)

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("<int:course_id>/lessons/", LessonListView.as_view(), name="lesson_list"),
    path(
        "<int:course_id>/lessons/<int:pk>/",
        LessonDetailView.as_view(),
        name="lesson_detail",
    ),
    path(
        "<int:course_id>/questions/", QuestionListView.as_view(), name="question_list"
    ),
    path("<int:course_id>/enroll/", enroll, name="enroll"),
    path("<int:course_id>/submit/", submit, name="submit"),
    path("<int:course_id>/<int:submission_id>/result/", show_exam_result, name="result"),

]

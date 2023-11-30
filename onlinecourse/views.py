from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from .models import (
    Course,
    Lesson,
    Instructor,
    Enrollment,
    Learner,
    Question,
    Submission,
    Choice,
)


class CourseListView(ListView):
    model = Course
    template_name = "onlinecourse/course_list.html"
    context_object_name = "courses"
    # I will add list of each course intructors to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lst_of_instructores = []
        lst_of_instructors_querysets = [course.instructor.all() for course in context["courses"]]
        for query in lst_of_instructors_querysets:
            for instructor in query:
                lst_of_instructores.append(instructor.user.username)

        context["instructors"] = lst_of_instructores
        context["str_user"] = str(self.request.user) # str_user to prevent confusion with user
        # the self.request.user may not be a learner
        try : 
            learner = Learner.objects.get(user=self.request.user)
            context["enrolled_courses_ids"] = Enrollment.objects.filter(learner=learner).values_list('course', flat=True)
        except :
            context["enrolled_courses_ids"] = []

        return context
    #    context["courses"] = Course.objects.all()

class CourseDetailView(DetailView):
    model = Course
    template_name = "onlinecourse/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_lessons"] = Lesson.objects.filter(course=self.object).exists()
        context["is_questions"] = Question.objects.filter(course=self.object).exists()
        return context


class LessonListView(ListView):
    model = Lesson
    template_name = "onlinecourse/lesson_list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        return Lesson.objects.filter(course__id=self.kwargs["course_id"])


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "onlinecourse/lesson_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = Course.objects.get(id=self.kwargs["course_id"])
        return context


class QuestionListView(ListView):
    model = Question
    template_name = "onlinecourse/question_list.html"

    def get_queryset(self):
        return Question.objects.filter(course__id=self.kwargs["course_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_id"] = self.kwargs["course_id"]
        context["course"] = Course.objects.get(id = self.kwargs["course_id"])
        return context


def extract_answers(request):
    answers = []
    for key, value in request.POST.items():
        if key.startswith("choice"):
            choice_id = int(value)
            answers.append(choice_id)
    return answers


def submit(request, course_id):
    course = Course.objects.get(pk=course_id)
    enrollment = Enrollment.objects.get(
        learner__user=request.user, course__id=course_id
    )
    submission = Submission(enrollment=enrollment)
    submission.save()
    choices = extract_answers(request)
    submission.choices.set(choices)
    submission_id = submission.id
    return HttpResponseRedirect(
        reverse("courses:result", args=(course_id, submission_id))
    )


def show_exam_result(request, course_id, submission_id):
    questions = Question.objects.filter(course__id=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    choices = submission.choices.all()
    total_grade = 0
    for question in questions:
        selected_choices = choices.filter(question=question)
        if question.is_graded(selected_choices):
            total_grade += question.grade
    total_available_grade = questions.aggregate(Sum("grade"))["grade__sum"]
    context = {}
    context["total_grade"] = total_grade
    context["questions"] = questions
    context["choices"] = choices
    context["grade"] = round((total_grade / total_available_grade)*100) if total_available_grade != 0 else 0
    return render(request, "onlinecourse/exam_result.html", context)


def enroll(request, course_id):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=course_id)
        learner, created = Learner.objects.get_or_create(user=request.user)
        enrollment, created = Enrollment.objects.get_or_create(learner=learner, course=course)
        enrollment.save()
        course.save() # to update the number of learners in the course

        return HttpResponseRedirect(reverse("courses:course_list"))
    else :
        return HttpResponseRedirect(reverse("account_login"))

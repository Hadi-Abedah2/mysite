from django.contrib import admin
from .models import Course, Lesson, Instructor, Enrollment, Learner, Question, Submission, Choice
# Register your models here.

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Instructor)
admin.site.register(Enrollment)
admin.site.register(Learner)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Choice)

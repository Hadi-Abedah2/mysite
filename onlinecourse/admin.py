from django.contrib import admin
from .models import Course, Lesson, Instructor, Enrollment, Learner, Question, Submission, Choice
# Register your models here.

#admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Instructor)
admin.site.register(Enrollment)
admin.site.register(Learner)
#admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Choice)

class LessonInline(admin.TabularInline):
    model = Lesson 
    extra = 5 

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5 

class ChoicesInline(admin.TabularInline):
    model = Choice
    extra = 4 
@admin.register(Course)
class Course(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    readonly_fields = ['total_enrollment', 'rating']

@admin.register(Question)
class Question(admin.ModelAdmin):
    inlines = [ChoicesInline]


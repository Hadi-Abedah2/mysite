from django.db import models
from django.db.models import Avg
from django.conf import settings

# Create your models here.


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    HUMAN = "HB"
    ROBOT = "RB"
    ALIEN = "AL"
    choices = (
        (HUMAN, "Human"),
        (ROBOT, "Robot"),
        (ALIEN, "Alien"),
    )
    occupation = models.CharField(
        max_length=20, choices=choices, default=HUMAN, null=False
    )
    social_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username + ", " + self.occupation


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=False)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="course_images/", blank=True, default="course_images/defaultcourse.jpg")
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructor = models.ManyToManyField(Instructor)
    learners = models.ManyToManyField(Learner, through="Enrollment")
    total_enrollment = models.IntegerField(default=0, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ", " + str(self.total_enrollment)

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)
        self.total_enrollment = self.learners.count()
        self.rating = self.enrollment_set.aggregate(Avg("rating"))[
            "rating__avg"
        ]  # the result is a dictionary
        # Save the instance again with specific fields to avoid recursion
        super(Course, self).save(update_fields=['total_enrollment', 'rating']) 

class CourseInstructor(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)  
    
    class Meta:
        unique_together = ('course', 'instructor')

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    rating = models.FloatField(default=5.00)

    class Meta:
        unique_together = ('learner', 'course')

class Question(models.Model):
    question = models.CharField(max_length=1000)
    grade = models.IntegerField(default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.question[:15]

    def is_graded(self, selected_choices):
        correct_choices_ids = sorted(list(self.choice_set.filter(is_correct=True).order_by('id').values_list('id', flat=True)))
        selected_correct_ids = sorted(list(self.choice_set.filter(is_correct=True, id__in=selected_choices).order_by('id').values_list('id', flat=True)))
        return correct_choices_ids == selected_correct_ids
        

class Choice(models.Model):
    text = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:15]

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
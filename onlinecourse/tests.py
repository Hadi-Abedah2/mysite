from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, Learner, Enrollment

# Create your tests here.

class CourseListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 3 course instances for testing
        number_of_courses = 3
        for course_id in range(number_of_courses):
            Course.objects.create(
                name=f'Course {course_id}',
                description=f'Description {course_id}',
                # ... other necessary fields ...
            )
    
        cls.user = get_user_model().objects.create_user(username='testuser', password='123')
        Learner.objects.create(user=cls.user)
    def setUp(self):
        self.client.login(username='testuser', password='123')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/courses/')  # Adjust URL as necessary
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('courses:course_list'))  # Use the correct URL name
        self.assertEqual(response.status_code, 200)

    def test_view_lists_all_courses(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['courses']) == 3)

    def test_correct_template_used(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onlinecourse/course_list.html')


class CourseDetialViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create a course instance for testing
        Course.objects.create(
            name='Course 1',
            description='Description 1',
            # ... other necessary fields ...
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/courses/1/')

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('courses:course_detail', kwargs={'pk': 1}))
    
    def test_correct_template_used(self):
        response = self.client.get(reverse('courses:course_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onlinecourse/course_detail.html')
        self.assertContains(response, 'Course 1')

    def test_view_uses_correct_context(self):
        response = self.client.get(reverse('courses:course_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('course' in response.context)
        

class LessonListViewTest(TestCase):
    pass 

class LessonDetailViewTest(TestCase):
    pass 

class QuestionListViewTest(TestCase):
    pass


class EnrollTest(TestCase):
    @classmethod 
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='123')
        cls.course = Course.objects.create(
            name='Course 1',
            description='Description 1',
            # ... other necessary fields ...
        )

    def test_enroll(self):
        self.client.login(username='testuser', password='123')
        response = self.client.get(reverse('courses:enroll', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.all().exists())
        #self.assertTrue(response.url.startswith('/courses/{self.course.id}/'))

        
        
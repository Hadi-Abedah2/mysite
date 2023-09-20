from django.views.generic import TemplateView
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name='home'
urlpatterns = [
    path("", TemplateView.as_view(template_name='home/index.html')),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/ads'), name='logout'),
]

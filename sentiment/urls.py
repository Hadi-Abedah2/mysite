from django.urls import path
from . import views
app_name = "sentiment"
urlpatterns = [
    path("", views.sentiment_view, name="sentiment_analyzer")
]

"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static # this for serving static files in development mode
import  django.contrib.auth.urls
urlpatterns = [
    path("control-panel/", admin.site.urls),
    path("ads/", include("ads.urls")),
    #path("accounts/", include("django.contrib.auth.urls")), this is very basic auth
    path("", include("home.urls")),
    path("sentiment/", include("sentiment.urls")),
    path('accounts/', include('allauth.urls')),
    path("courses/", include("onlinecourse.urls")),
    path("api/v1/", include("ads.API.urls")),

]


# adding on urlpatterns to serve static file as favicon to my webapp
from django.views.static import serve
import os
from django.conf import settings

urlpatterns += [
    path('favicon.ico',   #When someone accesses '/favicon.ico' on my website, this URL pattern will be matched(which browsers often do automatically to retrieve the site's favicon ).
        serve,            # Use Django's static file serving view for this purpose

        # A dictionary of arguments passed to the `serve` view.
        {
            # This tells the `serve` view which file we want to serve.
            'path': 'favicon.ico',
            'document_root': os.path.join(settings.BASE_DIR, 'mysite/static'),
        }
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





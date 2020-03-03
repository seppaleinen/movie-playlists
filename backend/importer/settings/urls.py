"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from importer import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('import/daily/tmdb/production/companies',              views.fetch_daily_production_companies),
    path('import/daily/tmdb/keywords',              			views.fetch_daily_keywords),
    path('import/daily/tmdb/persons',                           views.fetch_daily_persons),
    path('import/daily/tmdb/movies',                            views.fetch_daily_movies),

    path('import/tmdb/persons',                                 views.import_persons),
    path('import/tmdb/keywords',                                views.import_keywords),
    path('import/tmdb/movies',                                  views.import_movies),

    path('api/autocomplete/<str:query>',                        views.autocomplete),
    path('api/search/<str:query>/',                             views.search),

    path('health',                                              views.health),
]

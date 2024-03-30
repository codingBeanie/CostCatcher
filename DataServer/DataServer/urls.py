"""
URL configuration for DataServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from REST_API.endpoints.files import Files
from REST_API.endpoints.transactions import Transactions
from REST_API.endpoints.categories import Categories
from REST_API.endpoints.assignments import Assignments
from REST_API.endpoints.schema import Schema
from REST_API.endpoints.settings import Settings
from REST_API.endpoints.statistics import Statistics

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/transactions/', Transactions.as_view()),
    path('api/files/', Files.as_view()),
    path('api/schema/', Schema.as_view()),
    path('api/settings/', Settings.as_view()),
    path('api/categories/', Categories.as_view()),
    path('api/assignments/', Assignments.as_view()),
    path('api/statistics/', Statistics.as_view())
]

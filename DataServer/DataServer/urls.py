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
from REST_API.endpoints.settings import Settings
from REST_API.endpoints.statistics import Statistics
from REST_API.endpoints.datespan import Datespan
from REST_API.endpoints.users import *
from REST_API.endpoints.period import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/', Register.as_view()),
    path('auth/login/', Login.as_view()),
    path('auth/updatePassword/', UpdatePassword.as_view()),
    path('auth/passwordReset/', RequestPasswordReset.as_view()),
    path('auth/setnewpassword/', SetNewPassword.as_view()),
    path('auth/updateEmail/', UpateEmail.as_view()),
    path('auth/deleteUser/', DeleteUser.as_view()),
    path('api/transactions/', Transactions.as_view()),
    path('api/files/', Files.as_view()),
    path('api/settings/', Settings.as_view()),
    path('api/categories/', Categories.as_view()),
    path('api/assignments/', Assignments.as_view()),
    path('api/statistics/', Statistics.as_view()),
    path('api/period/default/', PeriodDefault.as_view()),
    path('api/period/list/years/', PeriodListYears.as_view()),
    path('api/period/list/months/', PeriodListMonths.as_view()),
    path('api/datespan/', Datespan.as_view())
]

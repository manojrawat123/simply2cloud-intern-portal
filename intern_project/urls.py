"""intern_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from intern_user.views import MyLogin,UserRegistrationView, MyProfile
from skills.views import MySkills
from company.views import CompanyRegistrationView
from available_skills.views import PostJobView
from jobs.views import JobPostView,JobSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", MyLogin.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path('profile/', MyProfile.as_view(), name="profile" ),
    path("company_register/",CompanyRegistrationView.as_view(), name="company-register-view"),
    path('skills/', MySkills.as_view(), name="skills" ),
    path('skills/<int:id>/', MySkills.as_view(), name="skills-by-id" ),
    path('available-skills/', PostJobView.as_view(), name="avaliable-skills-id" ),
    path('job-post/', JobPostView.as_view(), name="job-post" ),
    path('job-search/', JobSearchView.as_view(), name="job-search" ),
    path('job-post/<int:id>/', JobPostView.as_view(), name="job-post-get-of-company")
]
"""new_intern_project URL Configuration

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
from intern_user.views import MyLogin,UserRegistrationView, MyProfile,UnAutProfView,VerifybyEmail, ForgotPassword, ResetPassword
from skills.views import MySkills
from company.views import CompanyRegistrationView
from available_skills.views import PostJobView
from jobs.views import JobPostView,JobSearchView,JobsUnAuthGetView,JobAuthSearchView
from intern_profile_job.views import InternJobProfileView, InternJobUnAuthCompanyViewSearch,AuthCompanyUserSearchView
from intern_job_application.views import InternJobApplicationView
from django.conf.urls.static import static
from django.conf import settings
from intern_experience.views import InternExperienceView
from message.views import MessageView
from conversional.views import ConversitionalView

urlpatterns = [

    path('admin/', admin.site.urls),
    path("login/", MyLogin.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path('profile/', MyProfile.as_view(), name="profile" ),
    path('accounts/activate/<userid_encode>/<token>/', VerifybyEmail.as_view(), name="verify email"),
    path('reset-password/<userid_encode>/<token>/', ResetPassword.as_view(), name="Reset Password"),
    path('forgetpassword/', ForgotPassword.as_view(), name="forgot password email"),

    # Un Authorize 
    path('home-unauth/', UnAutProfView.as_view(), name="home-un-auth-view"),
    path('intern-unauth-search/', InternJobUnAuthCompanyViewSearch.as_view(), name="home-un-auth-view"),
    path('intern-unauth-search/<int:id>/', InternJobUnAuthCompanyViewSearch.as_view(), name="home-un-auth-view-id"),
    path('job-unauth-search/', JobsUnAuthGetView.as_view(), name="home-un-auth-view"),    
    path('intern-auth-search/', AuthCompanyUserSearchView.as_view(), name="home-un-auth-view"),
    path('intern-auth-search/<int:id>/', AuthCompanyUserSearchView.as_view(), name="home-un-auth-view-id"),
    path("company_register/",CompanyRegistrationView.as_view(), name="company-register-view"),
    path('skills/', MySkills.as_view(), name="skills" ),
    path('skills/<int:id>/', MySkills.as_view(), name="skills-by-id" ),
    path('available-skills/', PostJobView.as_view(), name="avaliable-skills-id" ),
    path('job-post/', JobPostView.as_view(), name="job-post" ),
    path('job-search/', JobSearchView.as_view(), name="job-search" ),
    path('job-search-auth/', JobAuthSearchView.as_view(), name="job-search-auth" ),
    path('job-post/<int:id>/', JobPostView.as_view(), name="job-post-get-of-company"),
    path('compleate-intern-job-profile/',InternJobProfileView.as_view(), name="job-profile"),
    path('compleate-intern-job-profile/<int:id>/',InternJobProfileView.as_view(), name="job-profile-update"),
    path('intern-job-apply/', InternJobApplicationView.as_view(), name="apply-job"),
    path('intern-job-apply/<int:id>/', InternJobApplicationView.as_view(), name="apply-job"),
    path('intern-experience/', InternExperienceView.as_view(), name="add-intern-xperience"),
    path('intern-experience/<int:id>/', InternExperienceView.as_view(), name="edit-or-delete-intern-xperience"),
    path('chat/', MessageView.as_view(), name="message"),
    path('chat/<int:user_id1>/', MessageView.as_view(), name="message"),
    path('conversiation/', ConversitionalView.as_view(), name="chat")
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
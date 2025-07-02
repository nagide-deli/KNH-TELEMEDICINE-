from django.urls import path
from .views import LoginView, SignupView, DoctorSignupView, DoctorSigninView, DoctorProfileView, LogoutView

urlpatterns = [
    path('signin/', LoginView. as_view(), name='signin'),
    path('signup/', SignupView. as_view(), name='signup'),
    path('doctor_signup/', DoctorSignupView. as_view(), name='doctorsignup'),
    path('doctor_signin/', DoctorSigninView. as_view(), name='doctor_signin'),
    path('doctorprofile/', DoctorProfileView.as_view(), name='doctor_profile_update'),
     path('logout/', LogoutView.as_view(), name='logout'),



]
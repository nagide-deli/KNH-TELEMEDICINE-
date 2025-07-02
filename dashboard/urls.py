from django.urls import path
from .views import dashboard


from . import views

urlpatterns = [
    path('landingpage/', views.landingpage, name='landingpage'),
    path('home/', dashboard, name='dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]
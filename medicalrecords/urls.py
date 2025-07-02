from django.urls import path
from .views import MedicalRecordListCreateView, MedicalRecordCreateView, medical_records_view

urlpatterns = [
    path('medical-records/', MedicalRecordListCreateView.as_view(), name='medical_records'),
    path('add-medical-record/', MedicalRecordCreateView.as_view(), name='add_medical_record'),
    path('medical-records/', medical_records_view, name='medical_record_list'),

]

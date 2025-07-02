from django.urls import path
from .views import (
    AppointmentCreateView,
    AppointmentListView,
    AppointmentDetailView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    AppointmentStatusUpdateView
)

urlpatterns = [
    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('createappointment/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointmentsupdate/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointmentsdelete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointments/<int:pk>/update-status/', AppointmentStatusUpdateView.as_view(),
         name='update_appointment_status'),

]

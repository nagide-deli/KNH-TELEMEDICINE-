from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Appointment


@shared_task
def send_appointment_reminders():
    upcoming_appointments = Appointment.objects.filter(time__gte=now(), time__lte=now() + timedelta(hours=1))

    for appointment in upcoming_appointments:
        subject = "Appointment Reminder"
        message = f"Dear {appointment.patient.first_name},\n\nThis is a reminder for your appointment with Dr. {appointment.doctor.first_name} at {appointment.scheduled_time}.\n\nThank you."
        send_mail(subject, message, "ivynagi28@gmail.com", [appointment.patient.email])


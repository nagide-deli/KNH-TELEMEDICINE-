from datetime import timedelta

from django.db import models
from django.conf import settings



class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]




    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointment')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=100, default='Pending')
    meeting_link = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.date} at {self.time}"


    @property
    def reminder_time(self  ):
        return self.time - timedelta(hours=1)
# Create your models here.

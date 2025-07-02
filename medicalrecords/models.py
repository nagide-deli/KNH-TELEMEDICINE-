from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medical_records")
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_records")
    date_created = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = models.TextField(blank=True, null=True)
    medical_file = models.FileField(upload_to='medical_records/', blank=True, null=True)  # File Upload

    def __str__(self):
        return f"Medical Record for {self.patient.first_name} {self.patient.last_name} - {self.date_created.strftime('%Y-%m-%d')}"

# Create your models here.

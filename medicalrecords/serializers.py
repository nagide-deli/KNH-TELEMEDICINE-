from rest_framework import serializers
from .models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    medical_file = serializers.FileField(required=False)  # Allow file uploads

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'date_created', 'diagnosis', 'prescription', 'notes', 'medical_file']
        read_only_fields = ['doctor', 'date_created']

from rest_framework import serializers
from .models import Appointment
import datetime
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date', 'time', 'status', 'reason', 'meeting_link']
        read_only_fields = ['status']  # Status should be updated by the doctor

    def validate(self, data):
        if data['date'] < datetime.date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return data

    def create(self, validated_data):
        validated_data['status'] = 'pending'  # Default status when creating an appointment
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure only doctors can update status
        request = self.context.get('request')
        if request and request.user.is_doctor:
            instance.status = validated_data.get('status', instance.status)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.meeting_link = validated_data.get('meeting_link', instance.meeting_link)

        instance.save()
        return instance
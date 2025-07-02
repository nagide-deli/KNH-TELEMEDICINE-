from django.shortcuts import render, redirect
from django.urls import reverse
from google.oauth2.credentials import Credentials
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment
from .serializers import AppointmentSerializer
from django.shortcuts import get_object_or_404
from authentication.models import CustomUser
from .utils import create_google_meet




class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctors = CustomUser.objects.filter(is_doctor=True)
        return render(request, 'schedule.html', {'doctors': doctors})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)


        if serializer.is_valid():

            appointment = serializer.save(patient=request.user)

            # If no Google creds, send user to googleauth login first
            if 'credentials' not in request.session:
                # store desired next URL so we can return here
                request.session['next_appointment_data'] = request.data
                return redirect(reverse('google_login'))


            try: 


                meet_link = create_google_meet(request, appointment)
                appointment.meeting_link = meet_link
                appointment.save()

            except Exception as e:
                logger.error(f"Error creating Google Meet link: {e}")
                serializer.errors['google_meet'] = ['Failed to create Google Meet link. Please try again.']
            if not serializer.errors:
                # If appointment is successfully created, redirect to appointment list
                return redirect('appointment_list')

            

        doctors = CustomUser.objects.filter(is_doctor=True)
        return render(request, 'schedule.html', {'doctors': doctors, 'errors': serializer.errors})


    
    def perform_create(self, serializer):
       serializer.save(patient=self.request.user)

       return redirect('appointment_list')
    

class AppointmentListView(generics.ListAPIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get (self,  request, *args, **kwargs):
        user = request.user
        if user.is_doctor:
            appointments = Appointment.objects.filter(doctor=user)
            return render(request, 'doctor_appointments.html', {'appointments': appointments})
        else:
            appointments = Appointment.objects.filter(patient=user)
            return render(request, 'appointments.html', {'appointments': appointments})

   

class AppointmentDetailView(generics.RetrieveAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.all()

class AppointmentUpdateView(generics.UpdateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user)

class AppointmentDeleteView(generics.DestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        Renders a confirmation page before deletion.
        """
        appointment = get_object_or_404(Appointment, id=pk, patient=request.user)
        return render(request, 'appointments.html', {'appointment': appointment})

    def post(self, request, pk, *args, **kwargs):
        """
        Deletes the appointment and redirects to the appointment list.
        """
        appointment = get_object_or_404(Appointment, id=pk, patient=request.user)
        appointment.delete()
        return redirect('appointment_list')


class AppointmentStatusUpdateView(generics.UpdateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow doctors to update status of their appointments
        return Appointment.objects.filter(doctor=self.request.user)

    def patch(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=kwargs['pk'], doctor=request.user)
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment status updated successfully!"})
        return Response(serializer.errors, status=400)


# Create your views here.

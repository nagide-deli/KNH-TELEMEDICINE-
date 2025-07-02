from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from rest_framework import generics, permissions
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from authentication.models import CustomUser
from appointments.models import Appointment
from django.shortcuts import get_object_or_404
# class MedicalRecordListCreateView(generics.ListCreateAPIView):
#     serializer_class = MedicalRecordSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser)  # Handle file uploads


#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:  # Doctors can see all records
#             return MedicalRecord.objects.all()
#         return MedicalRecord.objects.filter(patient=user)
#         # Patients only see their records

#     def perform_create(self, serializer):
#         serializer.save(doctor=self.request.user)

class MedicalRecordListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_doctor:  # Assuming you have a way to check if the user is a doctor
            records = MedicalRecord.objects.all()
        else:
            records = MedicalRecord.objects.filter(patient=user)
        return render(request, 'medicalrecords.html', {
            'records': records
        })

    def post(self, request, *args, **kwargs):

        if not request.user.is_doctor:
             return render(request, 'medicalrecords.html'), {
                'error': 'Only doctors can create medical records.'
            }



        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=request.user)
            return redirect('medical_records')  # Redirect to the list view after creation
        user = request.user
        records = MedicalRecord.objects.filter(patient=user) if not user.is_staff else MedicalRecord.objects.all()
        return render(request, 'medicalrecords.html', {
            'records': records,
            'errors': serializer.errors,
            'patient': request.user
        })

    

class MedicalRecordCreateView(LoginRequiredMixin, View):

    def get(self, request):
        if not request.user.is_doctor:
            return render(request, 'medicalrecords.html', {
                'error': 'Only doctors can create medical records.'
            })

        # Get only patients who had appointments with the doctor
        patient_ids = Appointment.objects.filter(doctor=request.user)\
                                         .values_list('patient_id', flat=True)\
                                         .distinct()
        patients = CustomUser.objects.filter(id__in=patient_ids, is_doctor=False)

        return render(request, 'add_medicalrecord.html', {
            'patients': patients
        })

    def post(self, request):
        if not request.user.is_doctor:
            return render(request, 'medicalrecords.html', {
                'error': 'Only doctors can create medical records.'
            })

        diagnosis = request.POST.get('diagnosis')
        prescription = request.POST.get('prescription')
        notes = request.POST.get('notes', '')
        medical_file = request.FILES.get('medical_file')

        patient_id = request.POST.get('patient')
        patient = get_object_or_404(CustomUser, id=patient_id, is_doctor=False)

        MedicalRecord.objects.create(
            patient=patient,
            doctor=request.user,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes,
            medical_file=medical_file
        )

        return redirect('medical_record_list')  # or your appropriate name


# Create your views here.

@login_required
def medical_records_view(request):
        user = request.user
        if user.is_doctor:  # Doctors see all records
            records = MedicalRecord.objects.all()
        else:  # Patients see only their records
            records = MedicalRecord.objects.filter(patient=user)

        return render(request, 'medicalrecords.html', {'records': records})

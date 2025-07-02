from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from appointments.models import Appointment



def landingpage(request):
    return render(request, 'landingpage.html')

@login_required
def dashboard(request):

    user = request.user
    upcoming_appointments = Appointment.objects.filter(patient=user, time__gte=now())

    return render(request, 'home.html', {'user': request.user})

@login_required
def doctor_dashboard(request):

    return render(request, 'doctor_dashboard.html', {'user': request.user})

# Create your views here.

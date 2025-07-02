from django.shortcuts import render
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse as HTTPResponse
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from django.views.decorators.csrf import csrf_exempt





@login_required
def payment_view(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id, patient=request.user) 

    return render(request, 'payment.html', {'appointment': appointment}) 


@csrf_exempt
@login_required
def mpesa_payment(request):
    if request.method != 'POST':
        phone_number = request.POST.get('phone_number')
        appointment_id = request.POST.get('appointment_id')

    appointment = Appointment.objects.get(id=appointment_id, patient=request.user)



    client = MpesaClient()
    phone_number = '0703448188'
    amount = 1  # Amount to be paid
    account_reference = 'Knh Telemedicine'
    transaction_desc = 'Payment for telemedicine services'
    callback_url = 'https://darajambili.herokuapp.com/express-payment'

    response = client.stk_push(
        phone_number, amount, account_reference, transaction_desc, callback_url
    )

    return HTTPResponse(f"Payment initiated: {response}")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, DoctorSignUpSerializer,DoctorSigninSerializer,DoctorProfileSerializer
from .models import DoctorProfile
from rest_framework import generics, permissions
from django.views import View
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect(reverse('signin'))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request):
        return render(request, 'signup.html')

class LoginView(APIView):
    def post(self, request):
        # Get email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard page
        else:
            messages.error(request, "Invalid email or password")
            return redirect('signin')


    def get(self, request):
            return render(request, 'signin.html')

class DoctorSignupView(APIView):
    def post(self, request):
        serializer = DoctorSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Doctor registered successfully"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return render(request, 'doctor_signup.html')


class DoctorProfileView(generics.UpdateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return DoctorProfile.objects.get(user=self.request.user)
        except DoctorProfile.DoesNotExist:
            return None  # Handle missing profile gracefully

    def get(self, request):
        profile = self.get_object()

        if profile is None:
            messages.error(request, "No doctor profile found. Please create your profile.")
            return redirect('doctor_profile_update')  # Redirect to profile creation page

        return render(request, 'doctorprofile.html', {'profile': profile})

    
class DoctorSigninView(APIView):
    def post(self, request):
        serializer = DoctorSigninSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user and user.is_doctor:
                login(request, user)
                return redirect('doctor_dashboard')
            return Response({"error": "Invalid credentials or not a doctor account"},
                            status=status.HTTP_400_BAD_REQUEST)
       
            
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
            return render(request, 'signin.html')
    

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Log out the user
        return redirect('landingpage')  # Redirect to the sign-in page after logout    


# Create your views here.

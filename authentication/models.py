from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_doctor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self):
        return self.email
class DoctorProfile(models.Model):
    objects = None
    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='doctor_profile', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization} "


# Create your models here.

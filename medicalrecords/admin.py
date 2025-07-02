from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_created')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name')
    list_filter = ('date_created',)

# Register your models here.

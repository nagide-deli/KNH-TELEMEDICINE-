from django.urls import path
from .views import educational_resources_list, add_educational_resource

urlpatterns = [
    path('educational-resources/', educational_resources_list, name='educational_resources_list'),
    path('add-educational-resource/', add_educational_resource, name='add_educational_resource'),
    ]

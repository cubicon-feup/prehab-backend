from django.shortcuts import render
from rest_framework import viewsets
from ..models.Patient import Patient
from ..serializers.Patient import PatientSerializer

class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
from django.shortcuts import render
from rest_framework import viewsets
from ..models.Doctor import Doctor
from ..serializers.Doctor import DoctorSerializer


class DoctorView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
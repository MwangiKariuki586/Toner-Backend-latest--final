import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from .models import *
from custom_auth.models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_list_or_404
from rest_framework.generics import GenericAPIView
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework.permissions import IsAdminUser

@permission_classes([IsAuthenticated])
class TonerRequestsView(generics.ListCreateAPIView):
    queryset = Toner_Request.objects.all().order_by("-id")
    serializer_class = Toner_RequestSerializer
    
    
 
    def post(self, request):
        serializer = Toner_RequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Check if the user is an admin
            user = request.user
            if user.is_superuser:
                # If the user is an admin, skip saving their data
                serializer.save()
                return Response({
                    'message': 'Toner request sent successfully',
                    'data_sent_from_frontend': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                # For normal users, prefill user details
                serializer.save()
                toner_request_data = serializer.data
                staff_id = toner_request_data.get('user_staffid', 'Unknown Staff ID')
                staff_name = toner_request_data.get('user_staffname', 'Unknown Staff Name')
                department = toner_request_data.get('user_department', 'Unknown Department')
                location = toner_request_data.get('user_location', 'Unknown Location')
                toner_id = toner_request_data.get('toner', None)
                

                # Email functionality
                try:
                    toner = Toner.objects.get(id=toner_id)
                    toner_name = toner.Toner_name
                except Toner.DoesNotExist:
                    toner_name = 'Unknown Toner Name'
          
                # Construct the email message
                subject = 'Toner Request'
                message = (
                    f'Hello, there is a new toner request from:\n'
                    f'Staff ID: {staff_id}\n'
                    f'Staff Name: {staff_name}\n'
                    f'Department: {department}\n'
                    f'Location: {location}\n'
                    f'For:\n'
                    f'Toner Name: {toner_name}\n'
                )
                email_from = 'rexdraymond@gmail.com'
                recipient_list = ['mwangikariuki586@gmail.com','mwangialex268@gmail.com']
                try:
                    # Send email
                    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                except Exception as e:
                    # Highlight: Logging the email sending issue
                    print(f"Error sending email: {e}")            # Highlight: Returning the serialized data for confirmation
                return Response({
                    'message': 'Toner request sent successfully',
                    'data_sent_from_frontend': serializer.data
                }, status=status.HTTP_201_CREATED)
        else:
            # Highlight: Returning detailed errors for better feedback
            return Response({
                'error': 'Toner request validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class TonerRequestsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Toner_Request.objects.all()
    serializer_class = Toner_RequestSerializer

@permission_classes([IsAuthenticated])
class TonersView(generics.CreateAPIView):
    queryset = Toner.objects.all()
    serializer_class = Toner_Serializer
    
    def get(self, request):
        toners = Toner.objects.all().order_by("-id")
        serializer = Toner_Serializer(toners, many=True)
        return Response({"Toners": serializer.data})
    
    def post(self, request):
        serializer = Toner_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@permission_classes([IsAuthenticated])
class TonerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Toner.objects.all()
    serializer_class = Toner_Serializer

    def get_object(self, pk_or_name):
        try:
            # Try to lookup by ID first
            return Toner.objects.get(pk=int(pk_or_name))
        except (Toner.DoesNotExist, ValueError):
            # If not found by ID, try to lookup by name
            try:
                return Toner.objects.get(Toner_name=pk_or_name)
            except Toner.DoesNotExist:
                raise Http404

    def get(self, request, pk_or_name, *args, **kwargs):
        try:
            toner = self.get_object(pk_or_name)
            serializer = Toner_Serializer(toner)
            return Response(serializer.data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk_or_name, *args, **kwargs):
        try:
            toner = self.get_object(pk_or_name)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = Toner_Serializer(toner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_or_name, *args, **kwargs):
        try:
            toner = self.get_object(pk_or_name)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        toner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated])
class PrintersView(generics.CreateAPIView):
    queryset = Printer.objects.all()
    serializer_class = Printer_Serializer
    def get(self, request):
        printers = Printer.objects.all().order_by("-id")
        serializer = Printer_Serializer(printers, many=True)
        return Response({"Printer": serializer.data})
    
    def post(self, request):
        serializer = Printer_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@permission_classes([IsAuthenticated])
class PrintersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Printer.objects.all()
    serializer_class = Printer_Serializer

    def get_object(self, pk_or_name):
        try:
            # Try to lookup by ID first
            return Printer.objects.get(pk=int(pk_or_name))
        except (Printer.DoesNotExist, ValueError):
            # If not found by ID, try to lookup by name
            try:
                return Printer.objects.get(Printer_name=pk_or_name)
            except Printer.DoesNotExist:
                raise Http404

    def get(self, request, pk_or_name, *args, **kwargs):
        try:
            printer = self.get_object(pk_or_name)
            serializer = Printer_Serializer(printer)
            return Response(serializer.data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk_or_name, *args, **kwargs):
        try:
            printer = self.get_object(pk_or_name)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = Printer_Serializer(printer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_or_name, *args, **kwargs):
        try:
            printer = self.get_object(pk_or_name)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        printer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated])
class DepartmentsView(generics.CreateAPIView):
    queryset = Kenindia_Department.objects.all()
    serializer_class = Departments_Serializer
    def get(self, request):
        departments = Kenindia_Department.objects.all().order_by("-id")
        serializer = Departments_Serializer(departments, many=True)
        return Response({"Departments": serializer.data})
    
    def post(self, request):
        serializer = Departments_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@permission_classes([IsAuthenticated])
class DepartmentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kenindia_Department.objects.all()
    serializer_class = Departments_Serializer

    def get_object(self, pk_or_name):
        try:
            # Try to lookup by ID first
            return Kenindia_Department.objects.get(pk=int(pk_or_name))
        except (Kenindia_Department.DoesNotExist, ValueError):
            # If not found by ID, try to lookup by name
            try:
                return Kenindia_Department.objects.get(Department_name=pk_or_name)
            except Kenindia_Department.DoesNotExist:
                raise Http404

    def get(self, request, pk_or_name, *args, **kwargs):
        try:
            department = self.get_object(pk_or_name)
            serializer = Departments_Serializer(department)
            return Response(serializer.data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk_or_name, *args, **kwargs):
        try:
            department = self.get_object(pk_or_name)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = Departments_Serializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_or_name, *args, **kwargs):
        try:
            department = self.get_object(pk_or_name)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated])
class LocationsView(generics.CreateAPIView):
    queryset = Kenindia_Location.objects.all()
    serializer_class = Location_Serializer
    def get(self, request):
        location = Kenindia_Location.objects.all().order_by("-id")
        serializer = Location_Serializer(location, many=True)
        return Response({"Locations": serializer.data})
    
    def post(self, request):
        serializer = Location_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@permission_classes([IsAuthenticated])
class LocationssDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kenindia_Location.objects.all()
    serializer_class = Location_Serializer

    def get_object(self, pk_or_name):
        try:
            # Try to lookup by ID first
            return Kenindia_Location.objects.get(pk=int(pk_or_name))
        except (Kenindia_Location.DoesNotExist, ValueError):
            # If not found by ID, try to lookup by name
            try:
                return Kenindia_Location.objects.get(Location_name=pk_or_name)
            except Kenindia_Location.DoesNotExist:
                raise Http404

    def get(self, request, pk_or_name, *args, **kwargs):
        try:
            location = self.get_object(pk_or_name)
            serializer = Location_Serializer(location)
            return Response(serializer.data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk_or_name, *args, **kwargs):
        try:
            location = self.get_object(pk_or_name)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = Location_Serializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_or_name, *args, **kwargs):
        try:
            location = self.get_object(pk_or_name)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
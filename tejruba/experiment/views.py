from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Experiment, Profile
from .forms import ExperimentForm, UserForm, ProfileForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.views.generic import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets, generics
from .serializers import ExperimentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
   #model = Experiment
@api_view(['GET', 'POST'])
def Experiments_list(request):
    """
    List all code experiments, or create a new experiment
    """
    if request.method == 'GET':
        experiments = Experiment.objects.all()
        serializer = ExperimentSerializer(experiments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExperimentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def Experiments_detail(request, pk):
    """
    Retrieve, update or delete experiment
    """
    try:
        experiment = Experiment.objects.get(pk=pk)
    except Experiment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ExperimentSerializer(experiment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExperimentSerializer(experiment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        experiment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

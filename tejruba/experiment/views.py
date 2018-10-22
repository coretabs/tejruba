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
from rest_framework.views import APIView,Response,status
from rest_framework import mixins


class ListExperiments(APIView):

    """
    List all experiments, or create a new experiment.
    """
    def get(self, request, format=None):
        experiments = Experiment.objects.all()
        serializer = ExperimentSerializer(experiments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ExperimentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateExperiment(APIView):

    """
    Retrieve, update or delete a experiment instance.
    """
    def get_object(self, pk):
        try:
            return Experiment.objects.get(pk=pk)
        except Experiment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        experiment = self.get_object(pk)
        serializer = ExperimentSerializer(experiment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ExperimentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        experiment = self.get_object(pk)
        experiment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
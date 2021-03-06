from .models import Experiment, Profile
from .serializers import ExperimentSerializer, UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.views import APIView,Response,status
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics

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
        experiment = self.get_object(pk)
        serializer = ExperimentSerializer(experiment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        experiment = self.get_object(pk)
        experiment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class useful(APIView):

    def useful(self, request, pk=None, post_pk=None):
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
            experiment = Experiment.objects.get(pk=pk)
            if experiment.usefuls.filter(id=request.user.id).exists():
                experiment.usefuls.remove(request.user)
                return Response("Usefuls has been removed")
            else:
                if experiment.usefuls.filter(id=request.user.id).exists():
                    experiment.usefuls.remove(request.user)
                experiment.usefuls.add(request.user)
                return Response("Usefuls has been added")


class notuseful(APIView):
    def notuseful(self, request, pk=None, post_pk=None):
        if not request.user.is_authenticated:
            return Response("Authentication credentials were not provided.")
        else:
            experiment = Experiment.objects.get(pk=pk)
            if experiment.notusefuls.filter(id=request.user.id).exists():
                experiment.notusefuls.remove(request.user)
                return Response("Not Usefuls has been removed")
            else:
                if experiment.notusefuls.filter(id=request.user.id).exists():
                    experiment.notusefuls.remove(request.user)
                experiment.notusefuls.add(request.user)
                return Response("Not Usefuls has been added")


class LoginView(APIView):
    serializer_class = LoginSerializer
    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data['user']
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        django_logout(request)

        return Response({'detail': _("تم تسجيل الخروج بنجاح")},
                        status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    """
    Create a User
    """
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

class UserDetail(APIView):
    """
    Retrieve a User
    """
    #queryset = User.objects.all()
    #serializer_class = UserSerializer
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
        serializer = UserSerializer(experiment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        experiment = self.get_object(pk)
        serializer = UserSerializer(experiment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        experiment = self.get_object(pk)
        experiment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
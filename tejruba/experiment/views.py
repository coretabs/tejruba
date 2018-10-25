from .models import Experiment, Profile
from .serializers import ExperimentSerializer, LoginSerializer
from django.http import Http404
from rest_framework.views import APIView,Response,status
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


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
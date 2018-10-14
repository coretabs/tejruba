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
from rest_framework import authentication, permissions, viewsets
from .serializers import ExperimentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#list of experiments
def experiments_list(request):
    experiments = Experiment.objects.all()
    return render(request, 'list_experiments.html', {'experiments': experiments})


# detail of experiment
def experiment_detail_view(request, pk):
    experiment_detail = get_object_or_404(Experiment, pk=pk)
    return render(request, 'experiment_detail.html', context={'experiment': experiment_detail})


# Useful
class ExperimentUsefulRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Experiment, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if obj.usefuls.filter(pk=user.pk):
                obj.usefuls.remove(user)
            else:
                if obj.notusefuls.filter(pk=user.pk):
                    obj.notusefuls.remove(user)
                obj.usefuls.add(user)
        return url_


# Useful API
class ExperimentUsefulAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        obj = get_object_or_404(Experiment, pk=pk)
        user = self.request.user
        updated = False
        useful = False

        if user.is_authenticated:
            if obj.usefuls.filter(pk=user.pk):
                obj.usefuls.remove(user)
                useful = False
            else:
                if obj.notusefuls.filter(pk=user.pk):
                    obj.notusefuls.remove(user)
                useful = True
                obj.usefuls.add(user)
            updated = True
        data = {
            "updated": updated,
            "useful": useful
        }

        return Response(data)


# Not Useful
class ExperimentNotUsefulRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Experiment, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if obj.notusefuls.filter(pk=user.pk):
                obj.notusefuls.remove(user)
            else:
                if obj.usefuls.filter(pk=user.pk):
                    obj.usefuls.remove(user)
                obj.notusefuls.add(user)
        return url_


# Not Useful API
class ExperimentNotUsefulAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        obj = get_object_or_404(Experiment, pk=pk)
        user = self.request.user
        updated = False
        notuseful = False

        if user.is_authenticated:
            if obj.notusefuls.filter(pk=user.pk):
                obj.notusefuls.remove(user)
                notuseful = False
            else:
                if obj.usefuls.filter(pk=user.pk):
                    obj.notusefuls.remove(user)
                notuseful = True
                obj.notusefuls.add(user)
            updated = True
        data = {
            "updated": updated,
            "notuseful": notuseful
        }
        return Response(data)


def create_experiment(request):
    if not request.user.is_authenticated:
        raise Http404

    form = ExperimentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('experiments_list')

    return render(request, 'experiment_form.html', {'form': form})


def experiment_update(request, pk):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Experiment, pk=pk)

    if instance.author != request.user:
        raise Http404

    form = ExperimentForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect(instance)

    return render(request, 'experiment_form.html', {"form": form,
                                                    "instance": instance})


def experiment_delete(request, pk):
    instance = get_object_or_404(Experiment, pk=pk)

    if request.user == instance.author:
        instance.delete()

    return redirect("experiments_list")


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('experiments_list')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    return render(request, 'profile_view.html', {'profile': profile})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('experiments_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class ExperimentList(viewsets.ModelViewSet):
    """
    List all experiments, or create a new experiments.
    """
    #def get(self, request, format=None):
    #    experiments = Experiment.objects.all()
    #    serializer = ExperimentSerializer(experiments, many=True)
    #    return Response(serializer.data)
    #
    #def post(self, request, format=None):
    #    serializer = ExperimentSerializer(data=request.data)
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def create(self, request):
        serializer = ExperimentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
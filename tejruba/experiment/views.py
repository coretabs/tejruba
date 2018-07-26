from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Experiment
from .forms import ExperimentForm, UserForm, ProfileForm


#list of experiments
def experiments_list(request):
    experiments = Experiment.objects.all()
    return render(request, 'list_experiments.html', {'experiments': experiments})


# detail of experiment
def experiment_detail_view(request, pk):
    experiment_detail = get_object_or_404(Experiment, pk=pk)
    return render(request, 'experiment_detail.html', context={'experiment': experiment_detail})


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
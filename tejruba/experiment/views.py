from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Experiment
from .forms import ExperimentForm


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

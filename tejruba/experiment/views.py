from django.shortcuts import render, redirect
from django.http import Http404
from .models import Experiment
from .forms import ExperimentForm


#list of experiments
def experiments_list(request, slug=None):
    experiments = Experiment.objects.all()
    return render(request, 'list_experiments.html', {'experiments': experiments})


# detail of experiment
def experiment_detail_view(request, pk):
        try:
            experiment_id = Experiment.objects.get(pk=pk)  # get id of experiment
        except Experiment.DoesNotExist:
            raise Http404("Experiment does not exist")

        return render(
            request,
            'experiment_detail.html',
            context={'experiment': experiment_id, }
        )


def create_experiment(request):
    if not request.user.is_authenticated:
        raise Http404

    form = ExperimentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('experiments_list')

    return render(request, 'create_experiment.html', {'form': form})


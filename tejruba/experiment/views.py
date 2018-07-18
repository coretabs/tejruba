from django.shortcuts import render
from .models import Experiment
from django.http import Http404


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

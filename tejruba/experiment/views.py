from django.shortcuts import render
from .models import Experiment, Useful, NotUseful
from django.http import Http404
# Create your views here.


def experiments_list(request, slug=None):
    experiments = Experiment.objects.all()
    return render(request, 'list_experiments.html', {'experiments': experiments})



def experiment_detail_view(request,pk):
        try:
            experiment_id=Experiment.objects.get(pk=pk)
        except Experiment.DoesNotExist:
            raise Http404("Experiment does not exist")

        return render(
            request,
            'experiment_detail.html',
            context={'experiment':experiment_id,}
        )
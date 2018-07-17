from django.shortcuts import render
from .models import Experiment, Useful, NotUseful
# Create your views here.


def experiments_list(request, slug=None):
    experiments = Experiment.objects.all()
    return render(request, 'list_experiments.html', {'experiments': experiments})
from django.urls import path
from . import views
'''
experiments/add
experiments/update/<int:pk>
experiments/delete/<int:pk>
'''
urlpatterns = [
    path('', views.experiments_list, name='experiments_list'),
    path('experiments/<int:pk>', views.experiment_detail_view, name='experiment-detail'),
    path('experiments/add', views.create_experiment, name="create_experiment")
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.experiments_list, name='experiments_list'),
    path('experiments_list/<int:pk>', views.experiment_detail_view, name='experiment-detail'),

]

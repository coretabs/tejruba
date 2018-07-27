from django.urls import path
from . import views
'''
experiments/add
experiments/<int:pk>/edit
experiments/<int:pk>/delete
'''
urlpatterns = [
    path('', views.experiments_list, name='experiments_list'),
    path('experiments/<int:pk>/', views.experiment_detail_view, name='experiment-detail'),
    path('experiments/<int:pk>/useful/', views.ExperimentUsefulRedirect.as_view(), name='experiment_useful'),
    path('experiments/<int:pk>/notuseful/', views.ExperimentNotUsefulRedirect.as_view(), name='experiment_notuseful'),
    path('experiments/add/', views.create_experiment, name="create_experiment"),
    path('experiments/<int:pk>/edit/', views.experiment_update, name="experiment_update"),
    path('experiments/<int:pk>/delete/', views.experiment_delete, name="experiment_delete"),
    path('user/', views.update_profile, name="profile"),
    path('signup/', views.signup, name='signup'),

]

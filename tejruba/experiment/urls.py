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
   
    path('post', views.experiment_list, name="create_experiment"),
    path('experiments/<int:pk>/edit/', views.experiment_update, name="experiment_update"),
    path('experiments/<int:pk>/delete/', views.experiment_delete, name="experiment_delete"),
   
    path('experiments/<int:pk>/useful/', views.ExperimentUsefulRedirect.as_view(), name='experiment_useful'),
    path('experiments/<int:pk>/notuseful/', views.ExperimentNotUsefulRedirect.as_view(), name='experiment_notuseful'),
   
    path('api/experiments/<int:pk>/useful/', views.ExperimentUsefulAPI.as_view(), name='experiment_api_useful'),
    path('api/experiments/<int:pk>/notuseful/', views.ExperimentNotUsefulAPI.as_view(), name='experiment_api_notuseful'),
   
    path('user/', views.update_profile, name="profile"),
    path('user/<slug>/', views.profile_view, name="profile_view"),
    path('signup/', views.signup, name='signup'),

]

from django.urls import path
from . import views
'''
experiments/add
experiments/<int:pk>/edit
experiments/<int:pk>/delete
'''
urlpatterns = [
    path('experiments/', views.ListExperiments.as_view()),
    path('experiments/<int:pk>', views.UpdateExperiment.as_view()),

]

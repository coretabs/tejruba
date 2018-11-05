from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
'''
experiments/add
experiments/<int:pk>/edit
experiments/<int:pk>/delete
'''
urlpatterns = [
    path('experiments/', views.ListExperiments.as_view()),
    path('experiments/<int:pk>', views.UpdateExperiment.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('create_user/', views.UserCreate.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
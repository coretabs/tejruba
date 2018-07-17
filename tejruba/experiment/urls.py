from django.urls import path
from . import views

urlpatterns = [
    path('', views.experiments_list, name='product_list'),

]

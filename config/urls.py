"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/url/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
"""
from django.contrib import admin
from django.urls import path

from calculator import views as calculator_views

urlpatterns = [
    path('', calculator_views.dashboard, name='dashboard'),
    path('calculator/', calculator_views.calculator, name='calculator'),
    path('history/', calculator_views.history, name='history'),
    path('calculation/<int:calc_id>/', calculator_views.history_detail, name='history_detail'),
    path('calculation/save/', calculator_views.save_calculation, name='save_calculation'),
    path('calculation/<int:calc_id>/delete/', calculator_views.delete_calculation, name='delete_calculation'),
    path('calculation/<int:calc_id>/payslip/', calculator_views.payslip_preview, name='payslip'),
    path('admin/', admin.site.urls),
]
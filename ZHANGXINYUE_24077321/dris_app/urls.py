# ZHANGXINYUE
# 24077321

from django.urls import path
from .views import *
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('report-disaster/', report_disaster, name='report_disaster'),
    path('request-aid/', request_aid, name='request_aid'),
    path('volunteer-registration/', volunteer_registration, name='volunteer_registration'),
    path('disaster-reports/', view_disaster_reports, name='view_disaster_reports'),
    path('manage-disaster-reports/', manage_disaster_reports, name='manage_disaster_reports'),
    path('verify-disaster-report/<int:report_id>/', verify_disaster_report, name='verify_disaster_report'),
    path('shelters/', view_shelters, name='view_shelters'),
    path('manage-shelters/', manage_shelters, name='manage_shelters'),
    path('add-shelter/', add_shelter, name='add_shelter'),
    path('edit-shelter/<int:shelter_id>/', edit_shelter, name='edit_shelter'),
    path('manage-aid-requests/', manage_aid_requests, name='manage_aid_requests'),
    path('assign-aid-request/<int:request_id>/', assign_aid_request, name='assign_aid_request'),
    path('volunteer-dashboard/', volunteer_dashboard, name='volunteer_dashboard'),
    path('authority-dashboard/', authority_dashboard, name='authority_dashboard'),
    path('citizen-dashboard/', citizen_dashboard, name='citizen_dashboard'),
]    
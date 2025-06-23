# ZHANGXINYUE
# 24077321

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.utils import timezone
from .models import DisasterReport, AidRequest, Shelter, VolunteerProfile, VolunteerAssignment, User, VolunteerSkill
from .forms import DisasterReportForm, AidRequestForm, ShelterForm, VolunteerRegistrationForm, CustomUserCreationForm, DisasterReportFilterForm
import datetime

def home(request):
    disaster_reports = DisasterReport.objects.filter(is_verified=True).order_by('-timestamp')[:5]
    active_shelters = Shelter.objects.filter(is_available=True)
    context = {
        'disaster_reports': disaster_reports,
        'active_shelters': active_shelters,
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            user.role = role
            user.phone_number = form.cleaned_data.get('phone_number')
            user.address = form.cleaned_data.get('address')
            user.save()
            
            if role == 'VOLUNTEER':
                VolunteerProfile.objects.create(volunteer=user)
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def report_disaster(request):
    if request.method == 'POST':
        form = DisasterReportForm(request.POST)
        if form.is_valid():
            disaster_report = form.save(commit=False)
            disaster_report.reporter = request.user
            disaster_report.save()
            messages.success(request, 'Your disaster report has been submitted!')
            return redirect('home')
    else:
        form = DisasterReportForm()
    return render(request, 'report_disaster.html', {'form': form})

@login_required
def request_aid(request):
    if request.method == 'POST':
        form = AidRequestForm(request.POST)
        if form.is_valid():
            aid_request = form.save(commit=False)
            aid_request.requester = request.user
            aid_request.save()
            messages.success(request, 'Your aid request has been submitted!')
            return redirect('home')
    else:
        form = AidRequestForm()
    return render(request, 'request_aid.html', {'form': form})

@login_required
def volunteer_registration(request):
    try:
        volunteer_profile = request.user.volunteer_profile
    except VolunteerProfile.DoesNotExist:
        volunteer_profile = VolunteerProfile.objects.create(volunteer=request.user)
    
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST, instance=volunteer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your volunteer profile has been updated!')
            return redirect('home')
    else:
        form = VolunteerRegistrationForm(instance=volunteer_profile)
    
    return render(request, 'volunteer_registration.html', {'form': form})

@login_required
def view_disaster_reports(request):
    reports = DisasterReport.objects.all().order_by('-timestamp')
    form = DisasterReportFilterForm(request.GET)
    
    if form.is_valid():
        disaster_type = form.cleaned_data.get('disaster_type')
        severity = form.cleaned_data.get('severity')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        is_verified = form.cleaned_data.get('is_verified')
        
        if disaster_type:
            reports = reports.filter(disaster_type=disaster_type)
        if severity:
            reports = reports.filter(severity=severity)
        if start_date:
            reports = reports.filter(timestamp__date__gte=start_date)
        if end_date:
            reports = reports.filter(timestamp__date__lte=end_date)
        if is_verified is not None:
            reports = reports.filter(is_verified=(is_verified == 'True'))
    
    return render(request, 'view_disaster_reports.html', {'reports': reports, 'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'AUTHORITY')
def manage_disaster_reports(request):
    reports = DisasterReport.objects.all().order_by('-timestamp')
    form = DisasterReportFilterForm(request.GET)
    
    if form.is_valid():
        disaster_type = form.cleaned_data.get('disaster_type')
        severity = form.cleaned_data.get('severity')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        is_verified = form.cleaned_data.get('is_verified')
        
        if disaster_type:
            reports = reports.filter(disaster_type=disaster_type)
        if severity:
            reports = reports.filter(severity=severity)
        if start_date:
            reports = reports.filter(timestamp__date__gte=start_date)
        if end_date:
            reports = reports.filter(timestamp__date__lte=end_date)
        if is_verified is not None:
            reports = reports.filter(is_verified=(is_verified == 'True'))
    
    return render(request, 'manage_disaster_reports.html', {'reports': reports, 'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'AUTHORITY')
def verify_disaster_report(request, report_id):
    report = get_object_or_404(DisasterReport, id=report_id)
    
    if request.method == 'POST':
        report.is_verified = True
        report.verified_by = request.user
        report.verification_time = timezone.now()
        report.save()
        messages.success(request, 'Report has been verified!')
        return redirect('manage_disaster_reports')
    
    return render(request, 'verify_disaster_report.html', {'report': report})

@login_required
@user_passes_test(lambda u: u.role == 'AUTHORITY')
def manage_shelters(request):
    shelters = Shelter.objects.all()
    return render(request, 'manage_shelters.html', {'shelters': shelters})

@login_required
@user_passes_test(lambda u: u.role == 'AUTHORITY')
def add_shelter(request):
    if request.method == 'POST':
        form = ShelterForm(request.POST)
        if form.is_valid():
            shelter = form.save()
            messages.success(request, 'Shelter added successfully!')
            return redirect('manage_shelters')
    else:
        form = ShelterForm()
    return render(request, 'add_shelter.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'AUTHORITY')
def edit_shelter(request, shelter_id):
    shelter = get_object_or_404(Shelter, id=shelter_id)
    if request.method == 'POST':
        form = ShelterForm(request.POST, instance=shelter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shelter updated successfully!')
            return redirect('manage_shelters')
    else:
        form = ShelterForm(instance=shelter)
    return render(request, 'edit_shelter.html', {'form': form, 'shelter': shelter})

@login_required
def view_shelters(request):
    shelters = Shelter.objects.filter(is_available=True)
    return render(request, 'view_shelters.html', {'shelters': shelters})

@login_required
@user_passes_test(lambda u: u.role == 'AUTHORITY')
def manage_aid_requests(request):
    requests = AidRequest.objects.all().order_by('-timestamp')
    return render(request, 'manage_aid_requests.html', {'requests': requests})

@login_required
@user_passes_test(lambda u: u.role == 'AUTHORITY')
def assign_aid_request(request, request_id):
    aid_request = get_object_or_404(AidRequest, id=request_id)
    volunteers = User.objects.filter(role='VOLUNTEER')
    
    if request.method == 'POST':
        volunteer_id = request.POST.get('volunteer')
        if volunteer_id:
            volunteer = get_object_or_404(User, id=volunteer_id)
            assignment = VolunteerAssignment.objects.create(
                authority=request.user,
                volunteer=volunteer,
                task_type='SUPPLY_DISTRIBUTION',
                description=f"Fulfill aid request: {aid_request.description}",
                location=aid_request.requester.address or "Unknown",
                gps_latitude=0,  # Placeholder
                gps_longitude=0,  # Placeholder
                start_time=timezone.now(),
                end_time=timezone.now() + datetime.timedelta(hours=4),
                aid_request=aid_request
            )
            aid_request.assigned_to = volunteer
            aid_request.save()
            messages.success(request, 'Volunteer assigned successfully!')
            return redirect('manage_aid_requests')
    
    return render(request, 'assign_aid_request.html', {'aid_request': aid_request, 'volunteers': volunteers})

@login_required
def volunteer_dashboard(request):
    volunteer = request.user
    assignments = VolunteerAssignment.objects.filter(volunteer=volunteer)
    return render(request, 'volunteer_dashboard.html', {'assignments': assignments})

@login_required
@user_passes_test(lambda u: u.role == 'AUTHORITY')
def authority_dashboard(request):
    total_reports = DisasterReport.objects.count()
    verified_reports = DisasterReport.objects.filter(is_verified=True).count()
    pending_reports = total_reports - verified_reports
    
    total_aid_requests = AidRequest.objects.count()
    fulfilled_requests = AidRequest.objects.filter(is_fulfilled=True).count()
    pending_requests = total_aid_requests - fulfilled_requests
    
    total_shelters = Shelter.objects.count()
    available_shelters = Shelter.objects.filter(is_available=True).count()
    
    context = {
        'total_reports': total_reports,
        'verified_reports': verified_reports,
        'pending_reports': pending_reports,
        'total_aid_requests': total_aid_requests,
        'fulfilled_requests': fulfilled_requests,
        'pending_requests': pending_requests,
        'total_shelters': total_shelters,
        'available_shelters': available_shelters,
    }
    
    return render(request, 'authority_dashboard.html', context)

@login_required
def citizen_dashboard(request):
    user_reports = DisasterReport.objects.filter(reporter=request.user)
    user_aid_requests = AidRequest.objects.filter(requester=request.user)
    
    context = {
        'user_reports': user_reports,
        'user_aid_requests': user_aid_requests,
    }
    
    return render(request, 'citizen_dashboard.html', context)    
# ZHANGXINYUE
# 24077321

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = (
        ('CITIZEN', 'Citizen'),
        ('VOLUNTEER', 'Volunteer'),
        ('AUTHORITY', 'Authority'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CITIZEN')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="dris_app_user_set",
        related_query_name="dris_app_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="dris_app_user_set",
        related_query_name="dris_app_user",
    )
class DisasterReport(models.Model):
    DISASTER_TYPES = (
        ('FLOOD', 'Flood'),
        ('LANDSLIDE', 'Landslide'),
        ('HAZE', 'Haze'),
        ('EARTHQUAKE', 'Earthquake'),
        ('FIRE', 'Fire'),
        ('OTHER', 'Other'),
    )
    SEVERITY_LEVELS = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    )
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    disaster_type = models.CharField(max_length=20, choices=DISASTER_TYPES)
    location = models.CharField(max_length=255)
    gps_latitude = models.FloatField()
    gps_longitude = models.FloatField()
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='verified_reports')
    verification_time = models.DateTimeField(blank=True, null=True)

class AidRequest(models.Model):
    AID_TYPES = (
        ('FOOD', 'Food'),
        ('WATER', 'Water'),
        ('SHELTER', 'Shelter'),
        ('MEDICAL', 'Medical'),
        ('RESCUE', 'Rescue'),
        ('CLOTHING', 'Clothing'),
        ('OTHER', 'Other'),
    )
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aid_requests')
    disaster_report = models.ForeignKey(DisasterReport, on_delete=models.CASCADE, related_name='aid_requests', blank=True, null=True)
    #aid_type = ArrayField(models.CharField(max_length=20, choices=AID_TYPES), size=10)
    aid_type = models.CharField(max_length=20, choices=AID_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_fulfilled = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_aid_requests')
    fulfillment_time = models.DateTimeField(blank=True, null=True)

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='managed_shelters')
    address = models.TextField()
    gps_latitude = models.FloatField()
    gps_longitude = models.FloatField()
    capacity = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    special_facilities = models.TextField(blank=True, null=True)
    #special_facilities = ArrayField(models.CharField(max_length=50), blank=True, null=True, size=10)

class VolunteerSkill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class VolunteerProfile(models.Model):
    volunteer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='volunteer_profile')
    skills = models.ManyToManyField(VolunteerSkill, related_name='volunteers')
    availability_start = models.TimeField(blank=True, null=True)
    availability_end = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    assigned_tasks_count = models.IntegerField(default=0)

class VolunteerAssignment(models.Model):
    TASK_TYPES = (
        ('RESCUE', 'Rescue'),
        ('RELOCATION', 'Relocation'),
        ('MEDICAL', 'Medical Assistance'),
        ('SUPPLY_DISTRIBUTION', 'Supply Distribution'),
        ('SHELTER_MANAGEMENT', 'Shelter Management'),
        ('OTHER', 'Other'),
    )
    
    authority = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_tasks')
    task_type = models.CharField(max_length=30, choices=TASK_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    gps_latitude = models.FloatField()
    gps_longitude = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completion_time = models.DateTimeField(blank=True, null=True)
    disaster_report = models.ForeignKey(DisasterReport, on_delete=models.SET_NULL, blank=True, null=True, related_name='volunteer_assignments')
    aid_request = models.ForeignKey(AidRequest, on_delete=models.SET_NULL, blank=True, null=True, related_name='volunteer_assignments')    
# Generated by Django 5.2.3 on 2025-06-23 13:58

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("CITIZEN", "Citizen"),
                            ("VOLUNTEER", "Volunteer"),
                            ("AUTHORITY", "Authority"),
                        ],
                        default="CITIZEN",
                        max_length=10,
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to.",
                        related_name="dris_app_user_set",
                        related_query_name="dris_app_user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="dris_app_user_set",
                        related_query_name="dris_app_user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="VolunteerSkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="DisasterReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "disaster_type",
                    models.CharField(
                        choices=[
                            ("FLOOD", "Flood"),
                            ("LANDSLIDE", "Landslide"),
                            ("HAZE", "Haze"),
                            ("EARTHQUAKE", "Earthquake"),
                            ("FIRE", "Fire"),
                            ("OTHER", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("location", models.CharField(max_length=255)),
                ("gps_latitude", models.FloatField()),
                ("gps_longitude", models.FloatField()),
                (
                    "severity",
                    models.CharField(
                        choices=[
                            ("LOW", "Low"),
                            ("MEDIUM", "Medium"),
                            ("HIGH", "High"),
                            ("CRITICAL", "Critical"),
                        ],
                        max_length=10,
                    ),
                ),
                ("description", models.TextField()),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_verified", models.BooleanField(default=False)),
                ("verification_time", models.DateTimeField(blank=True, null=True)),
                (
                    "reporter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reports",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "verified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="verified_reports",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AidRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "aid_type",
                    models.CharField(
                        choices=[
                            ("FOOD", "Food"),
                            ("WATER", "Water"),
                            ("SHELTER", "Shelter"),
                            ("MEDICAL", "Medical"),
                            ("RESCUE", "Rescue"),
                            ("CLOTHING", "Clothing"),
                            ("OTHER", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("description", models.TextField()),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_fulfilled", models.BooleanField(default=False)),
                ("fulfillment_time", models.DateTimeField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_aid_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "requester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="aid_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "disaster_report",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="aid_requests",
                        to="dris_app.disasterreport",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Shelter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.TextField()),
                ("gps_latitude", models.FloatField()),
                ("gps_longitude", models.FloatField()),
                ("capacity", models.IntegerField()),
                ("current_occupancy", models.IntegerField(default=0)),
                ("is_available", models.BooleanField(default=True)),
                (
                    "contact_person",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "contact_phone",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("special_facilities", models.TextField(blank=True, null=True)),
                (
                    "manager",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="managed_shelters",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VolunteerAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "task_type",
                    models.CharField(
                        choices=[
                            ("RESCUE", "Rescue"),
                            ("RELOCATION", "Relocation"),
                            ("MEDICAL", "Medical Assistance"),
                            ("SUPPLY_DISTRIBUTION", "Supply Distribution"),
                            ("SHELTER_MANAGEMENT", "Shelter Management"),
                            ("OTHER", "Other"),
                        ],
                        max_length=30,
                    ),
                ),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=255)),
                ("gps_latitude", models.FloatField()),
                ("gps_longitude", models.FloatField()),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("is_completed", models.BooleanField(default=False)),
                ("completion_time", models.DateTimeField(blank=True, null=True)),
                (
                    "aid_request",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="volunteer_assignments",
                        to="dris_app.aidrequest",
                    ),
                ),
                (
                    "authority",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "disaster_report",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="volunteer_assignments",
                        to="dris_app.disasterreport",
                    ),
                ),
                (
                    "volunteer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="volunteer_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VolunteerProfile",
            fields=[
                (
                    "volunteer",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="volunteer_profile",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("availability_start", models.TimeField(blank=True, null=True)),
                ("availability_end", models.TimeField(blank=True, null=True)),
                ("is_available", models.BooleanField(default=True)),
                (
                    "emergency_contact_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "emergency_contact_phone",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("assigned_tasks_count", models.IntegerField(default=0)),
                (
                    "skills",
                    models.ManyToManyField(
                        related_name="volunteers", to="dris_app.volunteerskill"
                    ),
                ),
            ],
        ),
    ]

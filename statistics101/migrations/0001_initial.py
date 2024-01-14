# Generated by Django 4.2.5 on 2023-10-27 01:31

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        max_length=150,
                        unique=True,
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
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
            name="Source",
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
                ("SourceType", models.IntegerField()),
                ("Author", models.CharField(max_length=100)),
                ("Editorial", models.BooleanField(default=False)),
                ("Title", models.CharField(db_index=True, max_length=100, unique=True)),
                (
                    "Year",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1850),
                            django.core.validators.MaxValueValidator(2100),
                        ]
                    ),
                ),
                (
                    "Month",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                    ),
                ),
                ("FullDate", models.DateField(blank=True)),
                ("Container", models.CharField(blank=True, max_length=100, null=True)),
                ("PagenumberFrom", models.IntegerField(blank=True, null=True)),
                ("PagenumberTo", models.IntegerField(blank=True, null=True)),
                ("Place", models.CharField(blank=True, max_length=100, null=True)),
                ("Publisher", models.CharField(max_length=100, null=True)),
                (
                    "ISBN10",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="ISBN10 has to be 10 numeric charaters",
                                regex="^\\d{10}$",
                            )
                        ],
                    ),
                ),
                (
                    "ISBN13",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="ISBN10 has to be 13 numeric charaters",
                                regex="^\\d{13}$",
                            )
                        ],
                    ),
                ),
                ("URL", models.URLField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="TSMeta",
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
                ("TSName", models.CharField(db_index=True, max_length=30, unique=True)),
                ("TSDesc", models.CharField(max_length=300)),
                (
                    "UserID",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="TS_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TSInt",
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
                ("Time", models.DateTimeField(default=django.utils.timezone.now)),
                ("DPInt", models.IntegerField(null=True)),
                (
                    "TSMetaID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="TS_Int_Meta",
                        to="statistics101.tsmeta",
                    ),
                ),
            ],
            options={
                "ordering": ("Time",),
            },
        ),
        migrations.CreateModel(
            name="TSFloat",
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
                ("Time", models.DateTimeField(default=django.utils.timezone.now)),
                ("DPFloat", models.FloatField(null=True)),
                (
                    "TSMetaID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="TS_Float_Meta",
                        to="statistics101.tsmeta",
                    ),
                ),
            ],
            options={
                "ordering": ("Time",),
            },
        ),
    ]

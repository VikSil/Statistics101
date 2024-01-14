from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

# ----------------------------------------------------------------------------
# Classes in this module define DB structures
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Non-dataset classes
# ----------------------------------------------------------------------------


def expire_date_default():
    """
    Function returns the default expiry time for User objects
    """
    exp_date = timezone.now() + timedelta(days=60)
    exp_date = exp_date.replace(hour=23, minute=59, second=59)
    return exp_date


class User(AbstractUser):
    """
    Model for user information
    """

    password = models.CharField(max_length=128, verbose_name="password")
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="last login")
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(
        error_messages={"unique": "A user with that username already exists."},
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
    email = models.EmailField(blank=True, max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField(default=expire_date_default)
    groups = models.ManyToManyField(
        blank=True, related_name="user_set", related_query_name="user", to="auth.group"
    )
    user_permissions = models.ManyToManyField(
        blank=True,
        related_name="user_set",
        related_query_name="user",
        to="auth.permission",
    )


class Source(models.Model):
    """
    Model to store sources that are referenced by the website
    """

    # Types: 1 - Book, 2 - Video, 3 - Publication, 4 - Website, 5 - Data Sets
    SourceType = models.PositiveSmallIntegerField(
        null=False,
        unique=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    Author = models.CharField(max_length=100, null=True, blank=True)
    Editorial = models.BooleanField(blank=False, default=False)
    Title = models.CharField(max_length=100, null=False, unique=True, db_index=True)
    Year = models.PositiveSmallIntegerField(
        blank=False,
        unique=False,
        default=timezone.now().year,
        validators=[MinValueValidator(1850), MaxValueValidator(2100)],
    )
    Month = models.IntegerField(
        blank=True,
        null=True,
        unique=False,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    FullDate = models.DateField(blank=True, null=True)
    Container = models.CharField(max_length=100, blank=True, null=True, unique=False)
    PagenumberFrom = models.PositiveSmallIntegerField(
        blank=True, null=True, unique=False
    )
    PagenumberTo = models.PositiveSmallIntegerField(blank=True, null=True, unique=False)
    Place = models.CharField(max_length=100, blank=True, null=True, unique=False)
    Publisher = models.CharField(max_length=100, blank=True, null=True, unique=False)
    ISBN10 = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^\d{10}$", message="ISBN10 has to be 10 numeric charaters"
            )
        ],
    )
    ISBN13 = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^\d{13}$", message="ISBN10 has to be 13 numeric charaters"
            )
        ],
    )
    URL = models.URLField(max_length=200, blank=True, null=True, unique=True)


# ----------------------------------------------------------------------------
# Dataset classes
# ----------------------------------------------------------------------------


class Sample(models.Model):
    """
    Model to store metadata about sample/population
    """

    sample_name = models.CharField(null=False, unique=True, max_length=50)
    sample_size = models.PositiveIntegerField()
    sample_type = (
        models.PositiveIntegerField()
    )  # 1- Timeseries; 2- Proportion; 3-Survey
    UserID = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sample_owner",
    )
    is_population = models.BooleanField(blank=False, default=False)
    population_size = models.PositiveIntegerField(blank=True, null=True)
    # upload_complete is set to true once the async data upload is finished successfully
    # set by save_df_as_timeseries, save_df_as_proportion and save_df_as_survey
    upload_complete = models.BooleanField(blank=False, default=False)
    upload_dt = models.DateTimeField(
        blank=False, null=False, auto_now_add=True, unique=False
    )
    update_dt = models.DateTimeField(blank=True, null=True, unique=False, auto_now=True)


class Variable(models.Model):
    """
    Model to store population/ sample variables
    """

    parent_id = models.ForeignKey(
        Sample, null=False, on_delete=models.CASCADE, related_name="variable"
    )
    variable_name = models.CharField(null=False, unique=False, max_length=50)
    is_numerical = models.BooleanField(blank=False, default=False)
    is_timeseries = models.BooleanField(blank=False, default=False)
    upload_dt = models.DateTimeField(
        blank=False, null=False, auto_now_add=True, unique=False
    )
    update_dt = models.DateTimeField(blank=True, null=True, unique=False, auto_now=True)


class Datapoint(models.Model):
    """
    Model to store individual datapoints
    """

    individual_id = models.CharField(null=False, unique=False, max_length=150)
    variable_id = models.ForeignKey(
        Variable, null=False, on_delete=models.CASCADE, related_name="datapoint"
    )
    variable_value = models.CharField(
        null=False, blank=False, unique=False, max_length=120
    )
    proportion = models.FloatField(
        null=True,
        blank=True,
        unique=False,
        validators=[MinValueValidator(0.0)],
    )
    timestamp = models.DateTimeField(blank=True, null=True, unique=False)
    upload_dt = models.DateTimeField(
        blank=False, null=False, auto_now_add=True, unique=False
    )
    update_dt = models.DateTimeField(blank=True, null=True, unique=False, auto_now=True)

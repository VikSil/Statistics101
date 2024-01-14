from django.contrib import admin

from .models import *

# ----------------------------------------------------------------------------
# Classes in this module define Admin interface
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Non-dataset classes
# ----------------------------------------------------------------------------


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_superuser",
        "last_login",
        "is_active",
        "date_joined",
        "date_expiration",
    )


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "SourceType",
        "Author",
        "Editorial",
        "Title",
        "Year",
        "Month",
        "FullDate",
        "Container",
        "PagenumberFrom",
        "PagenumberTo",
        "Place",
        "Publisher",
        "ISBN10",
        "ISBN13",
        "URL",
    )


# ----------------------------------------------------------------------------
# Dataset administration classes
# ----------------------------------------------------------------------------


class SampleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sample_name",
        "sample_size",
        "sample_type",
        "UserID",
        "is_population",
        "population_size",
        "upload_complete",
        "upload_dt",
        "update_dt",
    )


class VariableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "parent_pk",
        "parent_sample",
        "variable_name",
        "is_numerical",
        "is_timeseries",
        "upload_dt",
        "update_dt",
    )

    # Display both the PK and name of the parent Sample
    def parent_pk(self, instance):
        return instance.parent_id.id

    def parent_sample(self, instance):
        return instance.parent_id.sample_name


class DatapointAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "individual_id",
        "variable_pk",
        "variable_name",
        "variable_value",
        "proportion",
        "timestamp",
        "upload_dt",
        "update_dt",
    )

    # Display both the PK and name of the parent Variable
    def variable_pk(self, instance):
        return instance.variable_id.id

    def variable_name(self, instance):
        return instance.variable_id.variable_name


# Register all classes to be visible in the front-end
admin.site.register(User, UserAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(Datapoint, DatapointAdmin)

# Generated by Django 4.2.5 on 2023-11-24 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('statistics101', '0005_alter_source_month_alter_source_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.PositiveIntegerField()),
                ('variable_name', models.CharField(max_length=50, unique=True)),
                ('variable_description', models.CharField(blank=True, max_length=300, null=True)),
                ('is_numerical', models.BooleanField(default=False)),
                ('variable_mean', models.FloatField(null=True)),
                ('variable_median', models.FloatField(null=True)),
                ('variable_stdev', models.FloatField(null=True)),
                ('is_timeseries', models.BooleanField(default=False)),
                ('upload_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('parent_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_name', models.CharField(max_length=50, unique=True)),
                ('sample_description', models.CharField(blank=True, max_length=300, null=True)),
                ('sample_size', models.PositiveIntegerField()),
                ('upload_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('UserID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sample_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proportion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=120)),
                ('value_count', models.PositiveIntegerField()),
                ('value_proportion', models.FloatField(blank=True, null=True)),
                ('is_mode', models.BooleanField(default=False)),
                ('upload_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('variable_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proportion', to='statistics101.variable')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('population_name', models.CharField(max_length=50, unique=True)),
                ('population_description', models.CharField(blank=True, max_length=300, null=True)),
                ('population_size', models.PositiveIntegerField()),
                ('upload_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('UserID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='population_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Datapoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idividual_id', models.PositiveIntegerField()),
                ('value', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('upload_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('variable_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datapoint', to='statistics101.variable')),
            ],
        ),
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=70)),
                ('old_value', models.CharField(max_length=300)),
                ('new_value', models.CharField(max_length=300, null=True)),
                ('change_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('UserID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changed_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

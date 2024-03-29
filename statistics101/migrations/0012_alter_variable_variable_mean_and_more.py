# Generated by Django 4.2.5 on 2023-12-02 00:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("statistics101", "0011_alter_datapoint_idividual_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="variable",
            name="variable_mean",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="variable",
            name="variable_median",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="variable",
            name="variable_stdev",
            field=models.FloatField(blank=True, null=True),
        ),
    ]

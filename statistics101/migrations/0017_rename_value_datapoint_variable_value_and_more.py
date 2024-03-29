# Generated by Django 4.2.5 on 2023-12-04 21:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("statistics101", "0016_alter_variable_variable_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="datapoint",
            old_name="value",
            new_name="variable_value",
        ),
        migrations.AddField(
            model_name="datapoint",
            name="proportion_count",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="datapoint",
            name="proportion_perc",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="Proportion",
        ),
    ]

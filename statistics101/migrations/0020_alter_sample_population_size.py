# Generated by Django 4.2.5 on 2023-12-04 23:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "statistics101",
            "0019_remove_variable_parent_type_sample_is_population_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="sample",
            name="population_size",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

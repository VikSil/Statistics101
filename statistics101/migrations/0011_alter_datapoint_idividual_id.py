# Generated by Django 4.2.5 on 2023-11-30 22:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("statistics101", "0010_alter_variable_parent_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datapoint",
            name="idividual_id",
            field=models.CharField(max_length=150),
        ),
    ]

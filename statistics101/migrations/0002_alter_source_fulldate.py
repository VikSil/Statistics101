# Generated by Django 4.2.5 on 2023-10-27 01:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("statistics101", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="source",
            name="FullDate",
            field=models.DateField(blank=True, null=True),
        ),
    ]
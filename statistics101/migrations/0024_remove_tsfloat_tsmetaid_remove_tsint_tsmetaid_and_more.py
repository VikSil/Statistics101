# Generated by Django 4.2.5 on 2023-12-30 00:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("statistics101", "0023_alter_sample_userid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tsfloat",
            name="TSMetaID",
        ),
        migrations.RemoveField(
            model_name="tsint",
            name="TSMetaID",
        ),
        migrations.RemoveField(
            model_name="tsmeta",
            name="UserID",
        ),
        migrations.RemoveField(
            model_name="variable",
            name="variable_mean",
        ),
        migrations.RemoveField(
            model_name="variable",
            name="variable_median",
        ),
        migrations.RemoveField(
            model_name="variable",
            name="variable_stdev",
        ),
        migrations.DeleteModel(
            name="Audit",
        ),
        migrations.DeleteModel(
            name="TSFloat",
        ),
        migrations.DeleteModel(
            name="TSInt",
        ),
        migrations.DeleteModel(
            name="TSMeta",
        ),
    ]

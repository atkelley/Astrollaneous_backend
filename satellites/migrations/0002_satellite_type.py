# Generated by Django 4.2.4 on 2025-02-13 21:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("satellites", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="satellite",
            name="type",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.4 on 2025-02-13 20:45

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Satellite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("acronym", models.CharField(max_length=200)),
                ("title", models.CharField(max_length=200)),
                ("image_url", models.CharField(blank=True, max_length=200, null=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("text", models.TextField()),
                ("text_html", models.TextField(editable=False, null=True)),
            ],
            options={
                "ordering": ["-created_date"],
            },
        ),
    ]

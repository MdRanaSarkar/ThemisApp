# Generated by Django 4.2 on 2023-05-15 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AIPI_App", "0002_speechaudiofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="NudityImage",
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
                ("name", models.CharField(max_length=500)),
                (
                    "image",
                    models.FileField(null=True, upload_to="nnimg/", verbose_name=""),
                ),
            ],
        ),
    ]

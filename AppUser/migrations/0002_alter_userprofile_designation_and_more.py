# Generated by Django 4.1.7 on 2023-04-01 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AppUser", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="designation",
            field=models.CharField(
                choices=[("1", "NormalUser"), ("2", "Attorney")], max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="usergender",
            field=models.CharField(
                choices=[("Female", "Female"), ("Male", "Male"), ("Other", "Other")],
                max_length=10,
            ),
        ),
    ]

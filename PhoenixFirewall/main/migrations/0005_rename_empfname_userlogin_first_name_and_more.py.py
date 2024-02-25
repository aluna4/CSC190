# Generated by Django 4.2.7 on 2024-02-12 06:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_userlogin_empfname_userlogin_emplname"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userlogin",
            old_name="empfName",
            new_name="first_name",
        ),
        migrations.RenameField(
            model_name="userlogin",
            old_name="emplName",
            new_name="last_name",
        ),
        migrations.AddConstraint(
            model_name="userlogin",
            constraint=models.UniqueConstraint(
                fields=("employeeID",), name="unique_employeeID"
            ),
        ),
    ]
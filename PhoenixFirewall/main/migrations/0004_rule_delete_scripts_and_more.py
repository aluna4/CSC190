# Generated by Django 4.2.6 on 2024-04-14 03:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("main", "0003_scripts_employeeid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rule",
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
                ("employeeID", models.CharField(max_length=10)),
                ("rule_name", models.CharField(max_length=50)),
                ("source_zone", models.CharField(max_length=50)),
                ("source_ip", models.CharField(max_length=50)),
                ("destination_zone", models.CharField(max_length=50)),
                ("destination_ip", models.CharField(max_length=50)),
                ("application", models.CharField(max_length=50)),
                ("service", models.CharField(max_length=50)),
                ("action", models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name="scripts",
        ),
        migrations.RenameField(
            model_name="userlogin",
            old_name="user_pswd",
            new_name="password",
        ),
        migrations.RemoveField(
            model_name="userlogin",
            name="user_name",
        ),
        migrations.AddField(
            model_name="userlogin",
            name="first_name",
            field=models.CharField(default="John", max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userlogin",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="userlogin",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userlogin",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userlogin",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userlogin",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
        migrations.AddField(
            model_name="userlogin",
            name="last_name",
            field=models.CharField(default="Doe", max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userlogin",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddField(
            model_name="userlogin",
            name="username",
            field=models.CharField(default="JohnDoe", max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userlogin",
            name="zones",
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name="userlogin",
            name="create_date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="date created"),
        ),
        migrations.AlterField(
            model_name="userlogin",
            name="employeeID",
            field=models.CharField(
                max_length=8,
                unique=True,
                validators=[django.core.validators.RegexValidator(regex="^\\d{8}$")],
            ),
        ),
    ]
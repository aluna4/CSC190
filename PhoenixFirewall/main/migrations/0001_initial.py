# Generated by Django 4.2.6 on 2024-04-21 01:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='userlogIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(default='emp_FirstName', max_length=15)),
                ('last_name', models.CharField(default='emp_LastName', max_length=15)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=250)),
                ('employeeID', models.CharField(max_length=8, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\d{8}$')])),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('zones', models.JSONField(default=list)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_name', models.CharField(max_length=50)),
                ('source_zone', models.CharField(max_length=50)),
                ('source_ip', models.CharField(max_length=50)),
                ('destination_zone', models.CharField(max_length=50)),
                ('destination_ip', models.CharField(max_length=50)),
                ('application', models.CharField(max_length=50)),
                ('service', models.CharField(max_length=50)),
                ('action', models.CharField(max_length=50)),
                ('employeeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

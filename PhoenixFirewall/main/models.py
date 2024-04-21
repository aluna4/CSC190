from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# custom user manager for userlogIn model
class userlogInManager(BaseUserManager):
    # creates and saves a User with the given username and password
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        
        # create a new user instance
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # creates and saves a superuser with the given username and password
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


# user login model
class userlogIn(AbstractBaseUser, PermissionsMixin):
    # user fields
    first_name = models.CharField(max_length=15, default="emp_FirstName")  # holds employee first name
    last_name = models.CharField(max_length=15, default="emp_LastName")  # holds employee last name
    username = models.CharField(max_length=100, unique=True)  # holds username
    password = models.CharField(max_length=250)  # holds user password
    employeeID = models.CharField(max_length=8, unique=True, validators=[RegexValidator(regex=r'^\d{8}$')])  # holds employee 8 digit ID number
    create_date = models.DateTimeField("date created", auto_now_add=True)  # holds date of user created
    zones = models.JSONField(default=list)  # holds user zones
    is_staff = models.BooleanField(default=False)  # indicates if the user is a staff member
    is_superuser = models.BooleanField(default=False)  # indicates if the user is a superuser
    is_active = models.BooleanField(default=True)  # indicates if the user is active

    objects = userlogInManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'employeeID']

    def clean(self):
        # check that the password is at least 8 characters
        if len(self.password) < 8:
            raise ValidationError({'password': "Password must be at least 8 characters long"})

        # check that the password is not similar to the username
        if self.password.lower() in self.username.lower():
            raise ValidationError({'password': "Password cannot be the same as the username"})

    # overrides save method to go through the validate method first
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Employee: {self.employeeID}, Username = {self.username}"


# rule model
class Rule(models.Model):
    employeeID = models.ForeignKey(userlogIn, on_delete=models.CASCADE)  # foreign key to userlogIn model
    rule_name = models.CharField(max_length=50)  # holds the name of the rule
    source_zone = models.CharField(max_length=50)  # holds the source zone
    source_ip = models.CharField(max_length=50)  # holds the source IP address
    destination_zone = models.CharField(max_length=50)  # holds the destination zone
    destination_ip = models.CharField(max_length=50)  # holds the destination IP address
    application = models.CharField(max_length=50)  # holds the application
    service = models.CharField(max_length=50)  # holds the service
    action = models.CharField(max_length=50)  # holds the action

    def __str__(self):
        return f"Employee: {self.employeeID.employeeID} Rule Name = {self.rule_name}"

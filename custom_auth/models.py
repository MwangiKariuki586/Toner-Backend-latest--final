from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils import timezone

class Kenindia_Department(models.Model):
    Department_name = models.CharField(max_length = 500)
    time_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.Department_name
class Kenindia_Location(models.Model):
    Location_name = models.CharField(max_length = 500)
    time_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.Location_name
class Printer(models.Model):
    Printer_name = models.CharField(max_length = 500)
    time_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.Printer_name
class Toner(models.Model):
    Toner_name = models.CharField(max_length = 500,default = "")
    #printer_name = models.ForeignKey(Printer, null = True ,on_delete = models.SET_NULL)
    quantity = models.PositiveIntegerField(default = 0)
    time_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.Toner_name
class Toner_Request(models.Model):
    user_staffid = models.CharField(max_length=50, blank=True, null=True)
    user_staffname = models.CharField(max_length=255, blank=True, null=True)
    user_department = models.CharField(max_length=255, blank=True, null=True)
    user_location = models.CharField(max_length=255, blank=True, null=True)
    toner = models.ForeignKey(Toner, null=True, on_delete=models.SET_NULL)
    printer_name = models.ForeignKey(Printer, null = True ,on_delete = models.SET_NULL)
    issued = models.BooleanField(default = False)
    Date_of_request = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        # If the user-related fields are not set and there is a logged-in user, set them
        if not self.user_staffid and hasattr(self, '_request_user'):
            self.user_staffid = self._request_user.staffid
            self.user_staffname = self._request_user.staff_name
            self.user_department = self._request_user.department
            self.user_location = self._request_user.location
        super(Toner_Request, self).save(*args, **kwargs)
    @property
    def days_since_request(self):
        difference = timezone.now() - self.Date_of_request
        return difference.days
class CustomUserManager(BaseUserManager):
    def create_user(self, staffid, password=None, **extra_fields):
        if not staffid:
            raise ValueError('The staffid field must be set')
        user = self.model(staffid=staffid, **extra_fields)
        user.set_password(password)
        user.is_active = extra_fields.get('is_active', False)  # Set is_active to False by default
        user.save(using=self._db)
        return user

    def create_superuser(self, staffid, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(staffid, password, **extra_fields)

class CustomUser(AbstractUser):
    email = None
    first_name = None
    last_name = None
    username = None
    staffid = models.CharField(max_length=10, unique=True)
    staff_name = models.CharField(max_length=255)
    department = models.ForeignKey(Kenindia_Department,null = True ,on_delete = models.SET_NULL)
    location = models.ForeignKey(Kenindia_Location,null = True ,on_delete = models.SET_NULL)

    USERNAME_FIELD = 'staffid'
    REQUIRED_FIELDS = ['staff_name','department','location']
    objects = CustomUserManager()

    

    def __str__(self):
        return self.staffid

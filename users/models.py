from django.db import models
from django.contrib import auth
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    _user_has_perm,
)
from datetime import datetime
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have username")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        permissions = [
            ("add_manager", "Can add manager"),
            ("change_manager", "Can change manager"),
            ("delete_manager", "Can delete manager"),
            ("view_manager", "Can view manager"),
        ]

    name = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=20, unique=True)
    phone = models.CharField(unique=True, max_length=20, null=True, blank=True)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    national_id_img = models.ImageField(null=True)
    vehicle = models.CharField(max_length=20, null=True)

    is_deliveryman = models.BooleanField(default=False)
    is_approaved_by_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_moderator = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_root = models.BooleanField(default=False)
    
    is_restaurant = models.BooleanField(default=False)
    

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone", "national_id"]

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True

        if not self.is_active or self.is_anonymous:
            return False

        if obj is not None:
            return _user_has_perm(self, perm, obj)

        for backend in auth.get_backends():
            if backend.has_perm(self, perm):
                return True

        return False

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser or self.is_moderator


# Employee Settings
class EmployeeSettings(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        abstract = True
        permissions = [
            ("add_employeesettings", "Can add employee settings"),
            ("change_employeesettings", "Can change employee settings"),
            ("delete_employeesettings", "Can delete employee settings"),
            ("view_employeesettings", "Can view employee settings"),
        ]

    def __str__(self):
        return self.name


class Nationality(EmployeeSettings):
    pass


class MaritalStatus(EmployeeSettings):
    pass


class EmployeeType(EmployeeSettings):
    pass


class City(EmployeeSettings):
    pass


class CityDistrict(EmployeeSettings):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"district: {self.name} - city: {self.city}"


class Employee(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    RILIGION_CHOICES = [
        ("muslim", "Muslim"),
        ("christian", "Christian"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    gander = models.CharField(max_length=6, choices=GENDER_CHOICES, default="male")
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, default=1)
    religion = models.CharField(
        max_length=10, choices=RILIGION_CHOICES, default="muslim"
    )
    marital_status = models.ForeignKey(
        MaritalStatus, on_delete=models.SET_NULL, null=True, blank=True
    )
    birth_date = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True, default=0)
    phone = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    national_id = models.CharField(max_length=20, unique=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, default=None)
    district = models.ForeignKey(CityDistrict, on_delete=models.SET_NULL, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    emp_type = models.ForeignKey(
        EmployeeType, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def calculate_age(self):
        if self.birth_date and self.age is None:
            today = datetime.now().astimezone(settings.CAIRO_TZ).date()
            age = today.year - self.birth_date.year

            month_diff = today.month - self.birth_date.month
            day_diff = today.day - self.birth_date.day

            if month_diff < 0 or (month_diff == 0 and day_diff < 0):
                age -= 1
            self.age = max(age, 0)

    def save(self, *args, **kwargs):
        self.calculate_age()
        super(Employee, self).save(*args, **kwargs)


#  Moderators
class Moderator(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.user.is_moderator = True
        self.user.name = self.employee.name
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name}"

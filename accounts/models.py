from django.contrib.gis.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, phone=None, email=None, username=None, **kwargs):
        # if not phone:
        #     raise ValueError("Users must have an phone")

        user = self.model(
            phone=phone,
            username=username,
            email=email,
        )
        user.set_password(email)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, username=None, **kwargs):
        user = self.create_user(
            email=email,
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    date_joined = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_deliveryboy = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name="userprofile"
    )
    user_address = models.TextField(null=True, blank=True)
    address_loc = models.PointField(srid=4326, null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    office_loc = models.PointField(srid=4326, null=True, blank=True)
    alt_phone = models.CharField(null=True, blank=True)
    location = models.PointField(srid=4326, null=True, blank=True)
    cart = models.JSONField(null=True, blank=True)


class SavedLocations(models.Model):
    city = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    location = models.PointField(srid=4326, null=True, blank=True)

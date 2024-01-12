import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.forms.fields import BooleanField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class AddedByMixin(models.Model): 
    added_by = models.ForeignKey(
        'accounts.User',
        null=True,
        on_delete=models.SET_NULL,
        editable=False
    )
    added_on = models.DateTimeField(blank=True, null=True, editable=False)
    class Meta:
        abstract = True

class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super().save(**kwargs)

    class Meta:
        abstract = True

class TimeMixin(models.Model):
    created_date = models.DateField(auto_now=True, null=True)
    updated_date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        abstract = True

class AddressMixin(models.Model):
    address = models.CharField(max_length=128, help_text=_("Organization Address"))
    city = models.CharField(max_length=60)

    class Meta:
        abstract = True
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.confirmed_email = False
        user_obj.save()
        return user_obj

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save()


class User(AbstractUser, PermissionsMixin):
    ADMINISTRATOR = "ADMINISTRATOR"
    DISPATCH_ATTENDANT = "DISPATCH_ATTENDANT"
    DISPATCH_MANAGER = "DISPATCH_MANAGER"

    ROLE_CHOICES = (
        ("", "Select Role"),
        (ADMINISTRATOR, "Administrators"),
        (DISPATCH_ATTENDANT, "Dispatch Attendant"),
        (DISPATCH_MANAGER, "Dispatch Manager"),
    )

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Username"
    )
    active = models.BooleanField(
        default=False
    )  # allows login - set after email confirmation
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    confirmed_email = models.BooleanField(default=False)
    staff_id = models.CharField(
        max_length=20, blank=True, null=True, unique=True, verbose_name="Staff ID"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    # USERNAME_FIELD and password are required by default
    USERNAME_FIELD = "email"

    objects = UserManager()

    # the following are required for the createsuperuser command
    REQUIRED_FIELDS = ["first_name", "last_name","phone_number"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    def save(self, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super().save(**kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, null=True, blank=True
    )
    email = models.EmailField(max_length=150)
    bio = models.TextField(
        max_length=20000,
        null=True,
        blank=True,
    )
    state = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    zip_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    signup_confirmation = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super().save(**kwargs)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class Organization(AddressMixin, TimeMixin, models.Model):
    super_admin = models.ForeignKey(
        get_user_model(),
        related_name="organization_admin",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200, help_text=_("Organization Name"))
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4()
        super().save(**kwargs)

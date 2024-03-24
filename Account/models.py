import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify
from django_jalali.db.models import jDateTimeField

from Account.validators import validate_email
from Account.variables import Numbers as AccountNumbers
from Account.variables import Strings as AccountStrings
from Account.variables import ErrorTexts as AccountErrorTexts


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_phone, username=None, email=None, password=None, **extra_fields):
        if not mobile_phone:
            raise ValueError(AccountErrorTexts.only_available_with_mobile_phone)

        if not username:
            raise ValueError(AccountErrorTexts.only_available_with_username)

        user = self.model(mobile_phone=self.normalize_phone(mobile_phone), username=username,
                          email=self.normalize_email(email) if email else None, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_phone, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(AccountErrorTexts.is_staff_must_be_true_for_staff)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(AccountErrorTexts.is_staff_must_be_true_for_super_user)

        return self.create_user(mobile_phone, username, email, password, **extra_fields)

    def normalize_phone(self, mobile_phone):
        return ''.join(filter(str.isdigit, mobile_phone))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=AccountNumbers.username_max, unique=True,
                                verbose_name=AccountStrings.username)

    mobile_phone = models.CharField(max_length=AccountNumbers.mobile_phone_max, unique=True, blank=False,
                                    null=False, verbose_name=AccountStrings.mobile_phone)

    authentication_token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(max_length=AccountNumbers.email_max, unique=True,
                              validators=[validate_email], blank=True, null=True, verbose_name=AccountStrings.email)

    slug = models.SlugField(max_length=AccountNumbers.username_slug_max, verbose_name=AccountStrings.slug)

    is_staff = models.BooleanField(default=False, verbose_name=AccountStrings.is_staff)

    is_active = models.BooleanField(default=True, verbose_name=AccountStrings.is_active)

    date_joined = jDateTimeField(auto_now_add=True, editable=False, verbose_name=AccountStrings.date_joined)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.slug = slugify(self.username)
        self.username = self.username.lower()

    class Meta:
        verbose_name = AccountStrings.custom_user
        verbose_name_plural = AccountStrings.custom_users


class OTP(models.Model):
    otp_type_choices = (
        ("R", "register"),
        ("F", "register"),
    )

    username = models.CharField(max_length=AccountNumbers.username_max, blank=True, null=True)

    mobile_phone = models.CharField(max_length=AccountNumbers.mobile_phone_max)

    password = models.CharField(max_length=AccountNumbers.password_max)

    sms_code = models.CharField(max_length=AccountNumbers.sms_code_max)

    authentication_token = models.UUIDField(blank=True, null=True)

    uuid = models.CharField(max_length=AccountNumbers.uuid_4_token_max)

    slug = models.SlugField(max_length=AccountNumbers.username_slug_max, blank=True, null=True)

    otp_type = models.CharField(max_length=AccountNumbers.otp_type_max)

    class Meta:
        verbose_name = AccountStrings.otp
        verbose_name_plural = AccountStrings.otp_plural

    def __str__(self):
        return f"{self.mobile_phone}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

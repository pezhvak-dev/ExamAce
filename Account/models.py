import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify
from django_jalali.db.models import jDateTimeField, jDateField

from Account.validators import validate_email


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_phone, username=None, email=None, password=None, **extra_fields):
        if not mobile_phone:
            raise ValueError("شماره تلفن الزامی است.")

        if not username:
            raise ValueError("نام کاربری الزامی است.")

        user = self.model(mobile_phone=self.normalize_phone(mobile_phone), username=username,
                          email=self.normalize_email(email) if email else None, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_phone, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("None")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("None")

        return self.create_user(mobile_phone, username, email, password, **extra_fields)

    def normalize_phone(self, mobile_phone):
        return ''.join(filter(str.isdigit, mobile_phone))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=75, unique=True)

    mobile_phone = models.CharField(max_length=11, unique=True, blank=False, null=False)

    authentication_token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(max_length=254, unique=True, validators=[validate_email], blank=True, null=True, )

    full_name = models.CharField(max_length=100)

    about_me = models.TextField(blank=True, null=True)

    slug = models.SlugField(max_length=75)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    date_joined = jDateTimeField(auto_now_add=True, editable=False)

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
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class OTP(models.Model):
    otp_type_choices = (
        ("R", "ثبت نام"),
        ("F", "فراموشی رمز عبور"),
        ("D", "حذف حساب کاربری"),
    )

    username = models.CharField(max_length=75, blank=True, null=True)

    mobile_phone = models.CharField(max_length=11)

    password = models.CharField(max_length=100)

    sms_code = models.CharField(max_length=4)

    authentication_token = models.UUIDField(blank=True, null=True)

    uuid = models.UUIDField()

    slug = models.SlugField(max_length=75, blank=True, null=True)

    otp_type = models.CharField(max_length=1, choices=otp_type_choices)

    class Meta:
        verbose_name = "رمز یکبار مصرف"
        verbose_name_plural = "رمزهای یکبار مصرف"

    def __str__(self):
        return f"{self.mobile_phone}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

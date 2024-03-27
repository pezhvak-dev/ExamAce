from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Account.models import CustomUser, OTP


class CustomUserAdmin(UserAdmin):
    list_display = ('mobile_phone', 'username', 'is_staff', 'is_superuser', 'authentication_token', 'date_joined')

    list_editable = ('is_staff', 'is_superuser',)

    search_fields = ('mobile_phone', 'username',)

    readonly_fields = ('date_joined',)

    list_filter = ('is_staff',)

    list_per_page = 50

    ordering = ('-date_joined',)

    search_help_text = "جستجو بر اساس شماره تلفن همراه و نام کاربری"

    filter_horizontal = ()

    fieldsets = ()


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("username", "mobile_phone", "password", "sms_code", "uuid", "otp_type")

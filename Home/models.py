from django.db import models
from django_jalali.db.models import jDateTimeField


class HeroBanner(models.Model):
    title = models.CharField(max_length=1000, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="1300x400")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__hero_banner"
        verbose_name = "هیرو بنر (نامحدود)"
        verbose_name_plural = "هیرو بنرها (نامحدود)"


class Banner1(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="880x330")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_1"
        verbose_name = "بنر صفحه اصلی - پایین چرا سایت ما (اولین بنر سمت راست و دومین بنر سمت چپ) (2 بنر)"
        verbose_name_plural = "بنرهای صفحه اصلی - پایین چرا سایت ما (اولین بنر سمت راست و دومین بنر سمت چپ) (2 بنر)"


class Banner2(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="1300x400")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_2"
        verbose_name = "بنر پایین درباره اسم وبسایت چی میشنویم (1 بنر)"
        verbose_name_plural = "بنرهای پایین درباره اسم وبسایت چی میشنویم (1 بنر)"


class Banner3(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="880x330")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_3"
        verbose_name = "بنر صفحه اصلی - پایین آخرین آزمون‌‌ها (اولین بنر سمت راست و دومین بنر سمت چپ) (2 بنر)"
        verbose_name_plural = "بنرهای صفحه اصلی - پایین آخرین آزمون‌‌ها (اولین بنر سمت راست و دومین بنر سمت چپ) (2 بنر)"



class Banner4(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="880x330")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_4"
        verbose_name = "بنر صفحه آزمون - سمت راست آزمون (3 بنر)"
        verbose_name_plural = "بنرهای صفحه آزمون - سمت راست آزمون (3 بنر)"


class Banner5(models.Model):
    title = models.CharField(max_length=100, verbose_name="تیتر")

    link = models.URLField(blank=True, null=True, unique=True, verbose_name="لینک")

    file = models.FileField(upload_to="Home/HeroBanner/files", verbose_name="فایل", help_text="280x74")

    can_be_shown = models.BooleanField(default=True, verbose_name="مجوز نشان داده شدن دارد؟")

    created_at = jDateTimeField(auto_now_add=True, verbose_name="ایجاد شده در تاریخ")

    updated_at = jDateTimeField(auto_now=True, verbose_name="به‌روز‌رسانی شده در تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "home__banner_5"
        verbose_name = "بنر صفحه آزمون - سمت چپ آزمون (3 بنر)"
        verbose_name_plural = "بنرهای صفحه آزمون - سمت چپ آزمون (3 بنر)"

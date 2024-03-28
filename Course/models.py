from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField
from moviepy.editor import VideoFileClip

from utilities.useful_functions import humanize_video_duration


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')

    icon = models.ImageField(upload_to='Course/Category/icons/', verbose_name='آیکون')

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دسته بندی')


class VideoCourse(models.Model):
    course_types = (
        ('F', 'رایگان'),
        ('P', 'پولی'),
    )

    name = models.CharField(max_length=100, unique=True, verbose_name='نام دوره')

    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='دسته بندی')

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دوره')

    teacher = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name='استاد')

    cover_image = models.ImageField(upload_to='Course/VideoCourse/cover_images', verbose_name='عکس کاور')

    introduction_video = models.FileField(upload_to='Course/VideoCourse/introduction_video', verbose_name='فیلم مقدمه')

    has_been_finished = models.BooleanField(default=False, verbose_name='آیا دوره به پایان رسده؟')

    total_seasons = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد فصل‌ها')

    total_sessions = models.PositiveSmallIntegerField(default=0, blank=True, verbose_name='تعداد قسمت‌ها')

    total_duration = models.PositiveSmallIntegerField(default=0, blank=True, verbose_name='مجموع دقایق')

    prerequisites = models.ManyToManyField(to="self", blank=True, verbose_name='پیش نیاز دوره')

    participated_users = models.ManyToManyField(to="Account.CustomUser", blank=True, related_name="video_courses",
                                                verbose_name='کاربران ثبت نام شده')

    type = models.CharField(max_length=1, choices=course_types, default='F', verbose_name='نوع دوره')

    price = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')

    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد؟')

    discount_percentage = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف',
                                                           validators=[MaxValueValidator(100)])

    slug = models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به‌روز‌رسانی')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'video_course'
        verbose_name = 'دوره ویدئویی'
        verbose_name_plural = 'دوره‌های ویدئویی'


class VideoCourseObject(models.Model):
    video_course = models.ForeignKey(VideoCourse, on_delete=models.CASCADE, verbose_name="قسمت دوره فیلمی", blank=True,
                                     null=True)

    title = models.CharField(max_length=200, verbose_name="تیتر", blank=True, null=True)

    note = CKEditor5Field(config_name="extends", verbose_name="یادداشت", blank=True, null=True)

    season_number = models.PositiveSmallIntegerField(default=0, verbose_name="شماره فصل", blank=True, null=True)

    session_number = models.PositiveSmallIntegerField(default=0, verbose_name="شماره قسمت", blank=True, null=True)

    video_file = models.FileField(upload_to="Course/VideoCourse/tutorials", verbose_name="فایل ویدئو", blank=True, null=True)

    attachment = models.FileField(upload_to="Course/VideoCourse/attachments", verbose_name="فایل ضمیمه", blank=True,
                                  null=True)

    duration = models.CharField(max_length=20, default=0, verbose_name="زمان فیلم")

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            # Load the video file
            video_path = self.video_file.path
            clip = VideoFileClip(video_path)
            # Get the duration in seconds and save it
            self.duration = int(clip.duration)
            clip.close()
            # Update the model with the duration
            super().save(*args, **kwargs)
        except Exception as e:
            # Handle any exceptions, such as if the file is not found or is not a valid video file
            print(f"An error occurred while getting the duration of the video file: {e}")

    class Meta:
        db_table = 'video_course_object'
        verbose_name = 'جزئیات فیلم'
        verbose_name_plural = 'جزئیات فیلم'

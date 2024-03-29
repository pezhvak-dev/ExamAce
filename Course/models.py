from django.core.validators import MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField
from moviepy.editor import VideoFileClip


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')

    icon = models.ImageField(upload_to='Course/Category/icons/', verbose_name='آیکون')

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دسته بندی')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'category'
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی‌ها'


class VideoCourse(models.Model):
    course_payment_types = (
        ('F', 'رایگان'),
        ('P', 'پولی'),
    )

    course_status_types = (
        ('NS', 'هنوز شروع نشده'),
        ('IP', 'در حال برگزاری'),
        ('F', 'به اتمام رسیده'),
    )

    name = models.CharField(max_length=100, unique=True, verbose_name='نام دوره')

    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='دسته بندی')

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دوره')

    what_we_will_learn = CKEditor5Field(config_name="extends", max_length=500, verbose_name='چی یاد میگیریم؟')

    teacher = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name='مدرس',
                                related_name='video_courses')

    cover_image = models.ImageField(upload_to='Course/VideoCourse/cover_images', verbose_name='عکس کاور')

    introduction_video = models.FileField(upload_to='Course/VideoCourse/introduction_video', verbose_name='فیلم مقدمه')

    status = models.CharField(max_length=2, choices=course_status_types, verbose_name='وضعیت دوره', default='NS')

    total_seasons = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد فصل‌ها')

    total_sessions = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name='تعداد قسمت‌ها')

    total_duration = models.PositiveIntegerField(default=0, verbose_name='مدت دوره')

    prerequisites = models.ManyToManyField(to="self", blank=True, verbose_name='پیش نیاز دوره')

    participated_users = models.ManyToManyField(to="Account.CustomUser", blank=True, verbose_name='کاربران ثبت نام شده')

    type = models.CharField(max_length=1, choices=course_payment_types, default='F', verbose_name='نوع دوره')

    price = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت')

    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد؟')

    discount_percentage = models.PositiveSmallIntegerField(default=0, verbose_name='درصد تخفیف',
                                                           validators=[MaxValueValidator(100)])

    price_after_discount = models.PositiveSmallIntegerField(default=0, verbose_name='قیمت بعد از تخفیف')

    slug = models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به‌روز‌رسانی')

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.type == "F":
            self.price = self.price_after_discount = self.discount_percentage = self.has_discount = 0

        if self.has_discount:
            self.price_after_discount = self.price - (self.price * (self.discount_percentage / 100))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'video_course'
        verbose_name = 'دوره ویدئویی'
        verbose_name_plural = 'دوره‌های ویدئویی'


class VideoSeason(models.Model):
    number = models.PositiveSmallIntegerField(default=1, verbose_name="شماره فصل")

    name = models.CharField(max_length=75, verbose_name="اسم فصل")

    course = models.ForeignKey(to=VideoCourse, on_delete=models.CASCADE, verbose_name="دوره")

    def __str__(self):
        return f"{self.course.name} - {self.name} - {self.number}"

    class Meta:
        db_table = 'video_season'
        verbose_name = 'فصل ویدئو'
        verbose_name_plural = 'فصل‌های ویدئو'


class VideoCourseObject(models.Model):
    video_course = models.ForeignKey(VideoCourse, on_delete=models.CASCADE, verbose_name="دوره", blank=True,
                                     null=True)

    title = models.CharField(max_length=200, verbose_name="تیتر", blank=True, null=True)

    note = CKEditor5Field(config_name="extends", verbose_name="یادداشت", blank=True, null=True)

    season = models.ForeignKey(to=VideoSeason, on_delete=models.CASCADE, blank=True, null=True, verbose_name="فصل")

    can_be_sample = models.BooleanField(default=False, verbose_name="به عنوان نمونه تدریس انتخاب شود؟")

    video_file = models.FileField(upload_to="Course/VideoCourse/tutorials", verbose_name="فایل ویدئو", blank=True,
                                  null=True)

    attachment = models.FileField(upload_to="Course/VideoCourse/attachments", verbose_name="فایل ضمیمه", blank=True,
                                  null=True)

    duration = models.PositiveIntegerField(default=0, verbose_name="زمان فیلم")

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

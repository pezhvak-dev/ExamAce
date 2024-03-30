from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField
from hitcount.models import HitCount


class Tag(models.Model):
    name = models.CharField(max_length=75, unique=True, verbose_name='نام')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'news__tags'
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ‌ها'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    icon = models.ImageField(upload_to='News/Category/icons/', verbose_name='آیکون', blank=True, null=True)

    cover_image = models.ImageField(upload_to='News/Category/images', verbose_name='تصویر', blank=True, null=True)

    description = CKEditor5Field(config_name="extends", verbose_name='درباره دسته بندی')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'news__category'
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی‌ها'


class News(models.Model):
    author = models.ForeignKey(to="Account.CustomUser", on_delete=models.CASCADE, verbose_name='نویسنده')

    title = models.CharField(max_length=100, verbose_name='عنوان')

    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='دسته بندی')

    tags = models.ManyToManyField(to=Tag, verbose_name='تگ‌ها', blank=True, related_name='news')

    content = CKEditor5Field(config_name="extends", verbose_name="محتوا")

    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    cover_image = models.ImageField(upload_to='News/News/cover_images', verbose_name='تصویر کاور')

    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')

    updated_at = jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین به‌روز‌رسانی')

    class Meta:
        db_table = 'news__news'
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار'
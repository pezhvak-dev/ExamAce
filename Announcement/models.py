from uuid import uuid4

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db.models import jDateTimeField

from Account.models import CustomUser


class Announcement(models.Model):
    """
    A model for managing user notifications within the application.

    This model provides a flexible and robust framework for creating different
    types of notifications (safe, caution, danger), targeting specific
    user groups (global or private), and offering rich text formatting capabilities
    through the CKEditor5Field.

    Fields:
        title (CharField): A concise and informative notification title.
        message (CKEditor5Field): The notification's detailed content, supporting
        rich text formatting for enhanced user experience.
        users (ManyToManyField): A relationship to link notifications with
        specific CustomUser instances (blank=True allows for global notifications).
        created_at (jDateTimeField): An automatically populated field recording
        the notification's creation timestamp.
        mode (CharField): The notification's severity level (choices from mode_choices).
        visibility (CharField): The notification's target audience (choices from visibility_choices).
    """

    mode_choices = (
        ("S", "Safe"),
        ("C", "Caution"),
        ("D", "Danger"),
    )

    visibility_choices = (
        ("G", "Global"),
        ("P", "Private"),
    )

    uuid = models.UUIDField(default=uuid4, editable=False)

    title = models.CharField(max_length=100)

    message = CKEditor5Field(config_name='extends')

    image = models.ImageField(upload_to="Announcement/Announcement/image", blank=True, null=True)

    users = models.ManyToManyField(to=CustomUser, blank=True)

    created_at = jDateTimeField(auto_now_add=True)

    mode = models.CharField(max_length=1, choices=mode_choices)

    visibility = models.CharField(max_length=1, choices=visibility_choices)

    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'announcement'
        verbose_name = "اعلانیه"
        verbose_name_plural = "اعلانیه‌ها"

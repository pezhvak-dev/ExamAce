from django import forms

from .models import VideoCourseObject


class VideoCourseForm(forms.ModelForm):
    class Meta:
        model = VideoCourseObject
        fields = "__all__"

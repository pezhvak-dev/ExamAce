# Generated by Django 5.0.3 on 2024-04-11 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='is_blocked',
            field=models.BooleanField(default=False, verbose_name='آیا بلاک شده است؟'),
        ),
    ]
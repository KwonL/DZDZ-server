# Generated by Django 3.0.6 on 2020-05-26 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food', '0004_auto_20200524_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodgallery',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photos', to=settings.AUTH_USER_MODEL),
        ),
    ]

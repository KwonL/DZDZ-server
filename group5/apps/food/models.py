import os
from uuid import uuid4

from django.db import models


def gallery_image_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return f"food_gallery/{uuid4()}{ext}"


class FoodGallery(models.Model):
    type_choices = [
        ("아침", "아침"),
        ("점심", "점심"),
        ("저녁", "저녁"),
    ]

    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=gallery_image_path)
    type = models.CharField(max_length=10, choices=type_choices, default="아침")
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "food_gallery"

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

    user = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="photos",
        null=True,
    )
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=gallery_image_path)
    type = models.CharField(max_length=10, choices=type_choices, default="아침")
    name = models.CharField(max_length=255, blank=True)
    nutrient = models.ForeignKey(
        "Nutrient",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="foods",
    )

    class Meta:
        db_table = "food_gallery"


class Nutrient(models.Model):
    food_name = models.CharField(max_length=255)
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    salt = models.FloatField()
    kcal = models.FloatField()


class TargetNutrient(models.Model):
    user = models.OneToOneField(
        "user.User", on_delete=models.CASCADE, related_name="target_nutrient"
    )
    calorie = models.FloatField()
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()


class CharacterImage(models.Model):
    UNDER, NORMAL, OVER = 0, 1, 2
    type_choices = [(UNDER, "적음"), (NORMAL, "보통"), (OVER, "많음")]

    image = models.ImageField(upload_to=gallery_image_path)
    type = models.IntegerField(choices=type_choices, default=NORMAL)

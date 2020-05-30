from rest_framework import serializers
from apps.food.models import FoodGallery
from drf_extra_fields.fields import Base64ImageField


class GallerySerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    kcal = serializers.SerializerMethodField()

    def get_kcal(self, obj, **kwargs):
        return obj.nutrient.kcal if obj.nutrient else None

    class Meta:
        model = FoodGallery
        fields = "__all__"
        extra_kwargs = {"type": {"required": True}}

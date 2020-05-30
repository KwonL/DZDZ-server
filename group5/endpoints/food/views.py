import base64

import requests
from rest_framework.generics import ListCreateAPIView

from apps.food.models import FoodGallery, Nutrient

from .serializers import GallerySerializer


class GalleryListAPI(ListCreateAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return FoodGallery.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        file = base64.b64decode(self.request.data.get("image"))
        res = requests.post(
            "https://food-img-classifier.herokuapp.com/api/classify",
            files={"file": file},
        )
        if res.status_code == 200:
            name = res.json().get("class").replace("_", " ")
        nutrient = Nutrient.objects.filter(food_name=name).first()
        serializer.save(user=self.request.user, name=name, nutrient=nutrient)

import base64

import requests
from rest_framework.generics import ListCreateAPIView

from apps.food.models import FoodGallery

from .serializers import GallerySerializer


class GalleryListAPI(ListCreateAPIView):
    queryset = FoodGallery.objects.all()
    serializer_class = GallerySerializer

    def perform_create(self, serializer):
        file = base64.b64decode(self.request.data.get("image"))
        res = requests.post(
            "https://food-img-classifier.herokuapp.com/api/classify",
            files={"file": file},
        )
        if res.status_code == 200:
            name = res.json().get("class")
        serializer.save(name=name)

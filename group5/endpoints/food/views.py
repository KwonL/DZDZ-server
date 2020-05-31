import base64

import requests
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.food.models import FoodGallery, Nutrient

from .serializers import GallerySerializer


class HomeScreenAPI(APIView):
    def get(self, *args, **kwargs):
        user = self.request.user
        result = {"kor_name": user.kor_name}
        cnt = FoodGallery.objects.filter(user=user).count()
        # 3으로 나눴을 때 남는 음식을 가져옴
        start = cnt - cnt % 3 if cnt % 3 else cnt - 3
        foods = (
            FoodGallery.objects.select_related("nutrient")
            .filter(user=user)
            .order_by("id")[start:]
        )
        result.update(
            {"calories": [f.nutrient.kcal if f.nutrient else 0 for f in foods]}
        )

        return Response(result)


class GalleryListAPI(ListCreateAPIView):
    serializer_class = GallerySerializer
    pagination_class = None

    def get_queryset(self):
        return (
            FoodGallery.objects.select_related("nutrient")
            .filter(user=self.request.user)
            .order_by("-id")[:21]
        )

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


class GalleryDetailAPI(RetrieveDestroyAPIView):
    queryset = FoodGallery.objects.all()
    serializer_class = GallerySerializer
    lookup_field = "id"

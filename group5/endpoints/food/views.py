import base64

import requests
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.food.models import CharacterImage, FoodGallery, Nutrient

from .serializers import GallerySerializer


class HomeScreenAPI(APIView):
    def get(self, *args, **kwargs):
        user = self.request.user
        result = {"kor_name": user.kor_name}

        try:
            target = user.target_nutrient
        except Exception:
            target = None
        result.update(
            {
                "target_nutrients": {
                    "calorie": target.calorie if target else 0,
                    "carbohydrate": target.carbohydrate if target else 0,
                    "protein": target.protein if target else 0,
                    "fat": target.fat if target else 0,
                }
            }
        )

        cnt = FoodGallery.objects.filter(user=user).count()
        # 3으로 나눴을 때 남는 음식을 가져옴
        try:
            start = cnt - cnt % 3 if cnt % 3 else cnt - 3
            foods = (
                FoodGallery.objects.select_related("nutrient")
                .filter(user=user)
                .order_by("id")[start:]
            )
            result.update(
                {
                    "calories": [
                        f.nutrient.kcal if f.nutrient else 0 for f in foods
                    ],
                    "carbohydrate": sum(
                        [
                            f.nutrient.carbohydrate if f.nutrient else 0
                            for f in foods
                        ]
                    ),
                    "protein": sum(
                        [
                            f.nutrient.protein if f.nutrient else 0
                            for f in foods
                        ]
                    ),
                    "fat": sum(
                        [f.nutrient.fat if f.nutrient else 0 for f in foods]
                    ),
                }
            )

            if (
                sum(result.get("calories"))
                > result.get("target_nutrients", {}).get("calorie") * 1.2
            ):
                image = (
                    CharacterImage.objects.filter(type=CharacterImage.OVER)
                    .order_by("?")
                    .first()
                )
            elif (
                sum(result.get("calories"))
                < result.get("target_nutrients", {}).get("calorie") * 0.8
            ):
                image = (
                    CharacterImage.objects.filter(type=CharacterImage.UNDER)
                    .order_by("?")
                    .first()
                )
            else:
                image = (
                    CharacterImage.objects.filter(type=CharacterImage.NORMAL)
                    .order_by("?")
                    .first()
                )
            result.update(
                {"image": self.request.build_absolute_uri(image.image.url)}
            )
        except Exception as e:
            print(e)
            result.update(
                {
                    "calories": [],
                    "carbohydrate": 0,
                    "protein": 0,
                    "fat": 0,
                    "image": "",
                }
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

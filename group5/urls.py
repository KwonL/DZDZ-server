from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from endpoints.food import views as food_views
from endpoints.user import views as user_views


urlpatterns = [
    path("admin/", admin.site.urls),
]

# User
urlpatterns += [
    path("api/login", user_views.UserLoginAPI.as_view()),
]

# Food
urlpatterns += [
    path("api/food/gallery", food_views.GalleryListAPI.as_view()),
    path("api/home", food_views.HomeScreenAPI.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

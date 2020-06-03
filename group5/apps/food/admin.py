from django.contrib import admin

from .models import CharacterImage


@admin.register(CharacterImage)
class CharacterImageAdmin(admin.ModelAdmin):
    pass

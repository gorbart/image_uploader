from django.contrib import admin

from image_handler.models import Image


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)

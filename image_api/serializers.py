from rest_framework import serializers

from image_handler.models import Image
from users.models import ApiUser, Tier


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('name', 'upload_time', 'expiry_time', 'owner', 'image')


class ApiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUser
        fields = ('user', 'tier')


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ('name', 'thumbnail_sizes', 'can_get_original', 'can_generate_expiring_links')

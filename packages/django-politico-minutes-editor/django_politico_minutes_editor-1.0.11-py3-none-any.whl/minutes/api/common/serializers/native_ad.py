from minutes.models import NativeAd
from rest_framework import serializers

PIXEL_DELIMETER = '>|<'


class NativeAdSerializer(serializers.ModelSerializer):
    pixels = serializers.SerializerMethodField()

    def get_pixels(self, obj):
        if obj.pixels is not None:
            pixel_list = obj.pixels.split(PIXEL_DELIMETER)
            return pixel_list

        return []

    class Meta:
        model = NativeAd
        fields = (
            "id",
            "handle",
            "sponsor",
            "lede",
            "body",
            "image",
            "campaign_title",
            "campaign_link",
            "pixels"
        )

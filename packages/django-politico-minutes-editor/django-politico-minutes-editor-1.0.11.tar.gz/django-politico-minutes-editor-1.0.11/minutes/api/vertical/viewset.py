from rest_framework.response import Response
from rest_framework.decorators import action
from minutes.models import Vertical, Edition
from minutes.api.common.serializers import (
    VerticalEditionsSerializer,
    EditionLiveSerializer
)
from minutes.api.common.viewsets import BaseApiReadOnlyViewset


class VerticalViewset(BaseApiReadOnlyViewset):
    queryset = Vertical.objects.all()
    serializer_class = VerticalEditionsSerializer
    lookup_field = "slug"

    @action(detail=True, methods=["get"])
    def live(self, request, slug=None, pk=None):
        vertical = self.get_object()
        edition = Edition.objects.latest_live(vertical.id)

        return Response(
            EditionLiveSerializer(edition).data
        )

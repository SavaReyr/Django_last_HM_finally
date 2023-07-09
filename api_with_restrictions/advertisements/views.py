from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadonly


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = AdvertisementFilter
    permission_classes = [IsOwnerOrReadonly, ]


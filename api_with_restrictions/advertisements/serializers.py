from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from advertisements.models import Advertisement

token = '489629878d8afc0cc2e0b4049f8b9558033fa42a'


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at',
                  ]

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().update(instance, validated_data)

    def validate(self, data):
        """Метод для валидации. Вызываются при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        adv_open = Advertisement.objects.filter(creator=self.context["request"].user, status="OPEN").count()
        if self.context["request"].method == 'POST' and adv_open >= 10:
            raise serializers.ValidationError('Exceed max advertisement count with status = OPEN')

        if self.context["request"].method == 'PATCH' and adv_open >= 10 and data.get('status') == 'OPEN':
            raise serializers.ValidationError('Exceed max advertisement count with status = OPEN')

        return data

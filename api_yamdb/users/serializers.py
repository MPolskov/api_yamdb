from rest_framework import serializers
from django.core import validators

from .models import User

UNIQ_NAME_ERROR = 'Выберите другое имя пользователя'
ERROR_REGEX_MSG = 'Имя пользователя содержит недопустимые символы'
REGEX = r'^[\w.@+-]+\Z'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=User.EMAIL_MAX_LENGTH,
        required=True
    )
    username = serializers.RegexField(
        regex=REGEX,
        max_length=User.USERNAME_MAX_LENGTH,
        required=True,
        validators=(
            validators.RegexValidator(
                REGEX,
                ERROR_REGEX_MSG),
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                UNIQ_NAME_ERROR
            )
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

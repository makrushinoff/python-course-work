from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
import logging
from Puzzle.models import Boards

logger = logging.getLogger(__name__)


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = ('id', 'data')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = User.objects.get(username=attrs.get('username'))
        if user is None or not user.is_active:
            logger.warning('No active account found with the given credentials')
            raise AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data

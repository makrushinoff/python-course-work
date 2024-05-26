from rest_framework import serializers
from Puzzle.models import Boards, Users

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Boards
        fields=('id', 'data')
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=('id', 'login', 'password')
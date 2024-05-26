from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Puzzle.models import Boards, Users
from Puzzle.serializers import BoardSerializer, UserSerializer

@csrf_exempt
def getAllBoards(request):
    allBoards = Boards.objects.all()
    serializer = BoardSerializer(allBoards, many=True)
    return JsonResponse(serializer.data, safe=False)
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Puzzle.models import Boards, Users
from Puzzle.serializers import BoardSerializer, UserSerializer

@csrf_exempt
def getAllBoards(request, boardId = 0):
    if request.method == 'GET' and boardId == 0: 
        allBoards = Boards.objects.all()
        serializer = BoardSerializer(allBoards, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'GET' and id != 0:
        board = Boards.objects.get(id = boardId)
        serializer = BoardSerializer(board, many=False)
        return JsonResponse(serializer.data, safe=False)
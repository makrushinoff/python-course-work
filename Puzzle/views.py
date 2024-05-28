from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from Puzzle.models import Boards, Users
from Puzzle.serializers import BoardSerializer, UserSerializer
from Puzzle.calculations import Calculator

class ApiView(APIView):
    @csrf_exempt
    def getAllBoards(self, request, boardId = 0):
        if request.method == 'GET' and boardId == 0: 
            allBoards = Boards.objects.all()
            serializer = BoardSerializer(allBoards, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'GET' and id != 0:
            board = Boards.objects.get(id = boardId)
            serializer = BoardSerializer(board, many=False)
            return JsonResponse(serializer.data, safe=False)
 
    @csrf_exempt   
    def findCircleLoop(self, request):
        if request.method == "POST":
            requestBody = json.loads(request.body)
            print(requestBody)
            calculator = Calculator()
            solution = calculator.find_loop(requestBody['data'])
            if solution is not None:
                return JsonResponse({"data": solution}, safe=False)
            
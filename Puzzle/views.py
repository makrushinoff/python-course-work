import multiprocessing
import os
import threading

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import bcrypt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from Puzzle.models import Boards
from Puzzle.serializers import BoardSerializer, MyTokenObtainPairSerializer
from Puzzle.calculations import Calculator
from Puzzle.boardGenerator import BoardGenerator


class ApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id=0):
        if board_id == 0:
            all_boards = Boards.objects.all()
            serializer = BoardSerializer(all_boards, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif board_id != 0:
            board = Boards.objects.get(id=board_id)
            serializer = BoardSerializer(board, many=False)
            return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        board_generator = BoardGenerator(calculator=Calculator())
        processes = []
        for i in range(os.cpu_count()):
            print(f'Thread{i} started to generate boards...')
            process = multiprocessing.Process(target=board_generator.generate_boards())
            processes.append(process)
            process.start()
        for p in processes:
            p.join()
        return JsonResponse({"message": "success"})


class CalculationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_body = json.loads(request.body)
        print(request_body)
        calculator = Calculator()
        solution = calculator.find_loop(request_body['data'])
        if solution is not None:
            return JsonResponse({"data": solution}, safe=False)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    @csrf_exempt
    def register(self, request):
        register_body = json.loads(request.body)
        register_body['password'] = bcrypt.hashpw(register_body['password'].encode('utf-8'), bcrypt.gensalt()).decode(
            'utf-8')
        user = User.objects.create_user(username=register_body['login'], password=register_body['password'])
        user.save()
        return JsonResponse({"message": "success"})


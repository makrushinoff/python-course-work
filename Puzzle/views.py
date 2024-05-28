import datetime

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
import jwt

from Puzzle.models import Boards, Users
from Puzzle.serializers import BoardSerializer, UserSerializer
from Puzzle.calculations import Calculator
from Puzzle.boardGenerator import BoardGenerator


class ApiView(APIView):
    @csrf_exempt
    def boards_api(self, request, board_id=0):
        if request.method == 'GET' and board_id == 0:
            all_boards = Boards.objects.all()
            serializer = BoardSerializer(all_boards, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'GET' and id != 0:
            board = Boards.objects.get(id=board_id)
            serializer = BoardSerializer(board, many=False)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'POST':
            board_generator = BoardGenerator(calculator=Calculator())
            board_generator.generate_boards()
            return JsonResponse({"message": "success"})

    @csrf_exempt
    def find_circle_loop(self, request):
        if request.method == "POST":
            request_body = json.loads(request.body)
            print(request_body)
            calculator = Calculator()
            solution = calculator.find_loop(request_body['data'])
            if solution is not None:
                return JsonResponse({"data": solution}, safe=False)

    @csrf_exempt
    def register(self, request):
        register_body = json.loads(request.body)
        register_body['password'] = bcrypt.hashpw(register_body['password'].encode('utf-8'), bcrypt.gensalt()).decode(
            'utf-8')
        serializer = UserSerializer(data=register_body)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({"message": "success"})

    @csrf_exempt
    def authenticate(self, request):
        register_body = json.loads(request.body)
        user = Users.objects.get(login=register_body['login'])
        if user is None:
            raise AuthenticationFailed('User not found')

        if not bcrypt.checkpw(register_body['password'].encode('utf-8'), user.password.encode('utf-8')):
            raise AuthenticationFailed('Invalid password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        return JsonResponse({'token': token})

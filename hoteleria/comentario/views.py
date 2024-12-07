from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import *
from django.middleware.csrf import get_token

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Inicio de sesión exitoso"})
        else:
            return Response({"error": "Credeciales incorrectas"})
        

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Cierre de sesión exitoso"})
    

#@permission_classes([IsAuthenticated])

User = get_user_model()

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    #if not request.user.is_staff:
    #    return Response({'detail': 'No tienes permiso para regstrar usuarios'}, status=status.HTTP_403_FORBIDDEN)
    
    username = request.data.get('username')
    print(username)
    email = request.data.get('email')
    role = request.data.get("role")
    password = request.data.get('password')
 
    if not username or not email or not password:
        return Response({'detail': 'Todos los campos son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'El nombre de usuario ya esta en uso'}, status=status.HTTP_400_BAD_REQUEST)
    
    if role != "admin":
        user = User.objects.create_user(username=username, email=email, password=password)
    else:
        user = User.objects.create_superuser(username=username, email=email, role="admin", is_staff=True, password=password)

    return Response({'detail': 'Usuario registrado exitosamente'}, status=status.HTTP_201_CREATED)


def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'detail': 'Inicio de sesión exitoso'})
    else:
        return JsonResponse({'detail': 'Credenciales incorrectas'}, status=401)
    

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            'role': user.role,
            "is_staff": user.is_staff,
            "date_joined": user.date_joined,
        })

@csrf_exempt
@api_view(['POST'])
def registerWord(request):
    word = request.data.get('word')
    print(word)
    language = request.data.get('language')

    if Word.objects.filter(word=word).exists() and Word.objects.filter(language=language).exists():
        return Response({ 'detail': 'Palabra y lenguaje ya existente.'})
    else:
        words = Word.objects.create(word=word, language=language)
        return Response({ 'message': 'Guardado exitoso.'})


class UserDetailView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            return Response({
                'role': user.role,
            })
        except User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=404)


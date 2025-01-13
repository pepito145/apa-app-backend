from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserLogin, UsersInfos
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
import requests


from urllib.parse import unquote
from rest_framework.exceptions import NotFound


# Inscription
class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        # Vérifie si l'email existe déjà
        if UserLogin.objects.filter(email=email).exists():
            return Response({"error": "Email déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        if not all([email, password, first_name, last_name]):
            return Response({"error": "Tous les champs sont requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crée l'utilisateur
            user = UserLogin.objects.create(
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name
            )

            # Met à jour l'entrée dans users_infos
            if hasattr(user, 'infos'):
                user.infos.first_name = first_name
                user.infos.last_name = last_name
                user.infos.save()

            return Response({"message": "Utilisateur créé avec succès."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Erreur lors de l'inscription : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Connexion
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = UserLogin.objects.get(email=email)
            if check_password(password, user.password):
                # Génère un token JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "token": str(refresh.access_token)  # Retourne le token d'accès
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        except UserLogin.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)
        

class ClientID(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        try:
        # 查询 UserLogin 表中匹配的 email
            user = UserLogin.objects.get(email=email)
            return Response({'client_id': user.clientid})
        except UserLogin.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=404)
        
        
        
        
        
class Get_code(APIView):
    def get(self, request):
        # 获取并解码参数
        code = request.GET.get('code')
        state = request.GET.get('state')

        if not code or not state:
            return Response({'error': 'Missing code or state'}, status=400)

        try:
            # 尝试查找用户
            user = UserLogin.objects.get(clientid=state)
            user.code = code
            user.save()  # 保存 code 到数据库
            
            access_token=self.request_access_token(code, user)
            
            
            
            return Response({'code': code, 'state': state,'access_token':access_token,})
        except UserLogin.DoesNotExist:
            # 用户未找到，返回 404 错误
            raise NotFound({'error': f'User with id {state} not found'})

        except Exception as e:
            # 捕获其他可能的异常，返回 500 错误
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=500)
        
        
    def request_access_token(self, code, user):
        url = "https://wbsapi.withings.net/v2/oauth2"  # 替换为目标地址
        payload = {
            'action' : "requesttoken",
            'client_id' : user.clientid,
            'client_secret' : user.client_secret,
            'grant_type' : "authorization_code",
            'code': code,
            'redirect_uri' : "https://a428-193-54-192-76.ngrok-free.app/backend/api/get_token/",
            'state' : user.clientid,
        }
        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload)        
            data = response.json()
            #user = UserLogin.objects.get(clientid=response.state)
            # 更新用户的 token
            user.access_token = data['access_token']
            user.save()
            return data['access_token']
        except Exception as e:
            return {
                'error': 'Exception',
                'details': str(e),
            }
            
            
class Get_token(APIView):
    def get(self, request):
        access_token = request.GET.get('access_token')
        refresh_token = request.GET.get('refresh_token')
        
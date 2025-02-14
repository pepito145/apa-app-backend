from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserLogin, UsersInfos, Activity, Seance
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
import logging
from urllib.parse import unquote
from rest_framework.exceptions import NotFound
from django.utils import timezone

logger = logging.getLogger('django')
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
        

class Client_id(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        try:
        # 查询 UserLogin 表中匹配的 email
            user = UserLogin.objects.get(email=email)
            return Response({'client_id': user.client_id})
        except UserLogin.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=404)
        
        

        
        
class Get_code(APIView):
    def get(self, request):
        # 获取并解码参数
        code = request.GET.get('code')
        state = request.GET.get('state')
        
        logger.debug("request: ",request)
        logger.debug("state: ",state)
        
        if not code or not state:
            return Response({'error': 'Missing code or state'}, status=400)

        try:
            # 尝试查找用户
            user = UserLogin.objects.get(client_id=state)
            user.code = code
            
            user.save()  # 保存 code 到数据库
            
            access_token=self.request_access_token(code, user)
            self.notify(access_token)
            
            return Response({'code': code, 'state': state,'access_token':access_token,})
        except UserLogin.DoesNotExist:
            # 用户未找到，返回 404 错误
            raise NotFound({'error': f'User with id {state} not found','reçu':request.json()})

        except Exception as e:
            # 捕获其他可能的异常，返回 500 错误
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=500)
        
        
    def request_access_token(self, code, user):
        url = "https://wbsapi.withings.net/v2/oauth2"  # 替换为目标地址
        payload = {
            'action' : "requesttoken",
            'client_id' : user.client_id,
            'client_secret' : user.client_secret,
            'grant_type' : "authorization_code",
            'code': code,
            'redirect_uri' : "https://5aaf-193-54-192-76.ngrok-free.app/backend/api/get_code/",
        }
        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload)        
            data = response.json()

            user.access_token = data['body']['access_token']
            user.refresh_token = data['body']['refresh_token']
            user.user_id = data['body']['userid']
            user.save()
            
            return data['access_token']
        except Exception as e:
            return {
                'error': 'Exception',
                'details': str(e),
                'payload' : payload,
                'data' : data,
            }

    def notify(self, access_token):
        url = "https://wbsapi.withings.net/notify"
        payload = {
            'action' : "get",
            'callbackurl' : "https://5aaf-193-54-192-76.ngrok-free.app/backend/api/get_activity/",
        }
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload, headers=headers)        
            data = response.json()

            return None
        except Exception as e:
            return {
                'error': 'Exception'}


            
class post_step(APIView):
    def get(self, request):
        url = 'https://wbsapi.withings.net/v2/measure'
        payload = {
            'action' : "getactivity",
        }
        
class get_seance(APIView):
    def post(self, request):
        email= request.data.get('painLevel')
        painLevel = request.data.get('painLevel')
        difficulty = request.data.get('difficulty')
        totalExercises = request.data.get('totalExercises')
        time = request.data.get('time')

        seance = Seance.objects.create(
                email=email,
                painLevel = painLevel,
                difficulty = difficulty,
                totalExercises = totalExercises,
                time = datetime.fromtimestamp(time).date(),
            )
        seance.save()

class Get_activity(APIView):
    def post(self, request):
        try:

            logger.debug(dict(request.POST))
            
            user_id = request.POST.get('userid')
            appli = request.POST.get('appli')
            date = request.POST.get('date')
            logger.debug("+++++++++++++++++++++++++++ new activity +++++++++++++++++++++++++++++++++++")
            if int(appli)==16:
                logger.debug("+++++++++++++++++++++++++++ try to pull workout +++++++++++++++++++++++++++++++++++")
                user = UserLogin.objects.get(user_id=user_id)
                url = "https://wbsapi.withings.net/v2/measure"
                payload = {
                    'action' : "getworkouts",
                    'lastupdate' : int(timezone.now().timestamp())-500,
                    'data_fields' : "calories,intensity,hr_average,hr_min,hr_max,pause_duration,algo_pause_duration,spo2_average,steps,distance,elevation",
                }
                logger.debug("+++++++++++++++++++++++++++ call refresh token function +++++++++++++++++++++++++++++++++++")
                refresh_token(user)
                headers = {
                    'Authorization': f'Bearer {user.access_token}'
                }
                try:
                    # 发送 POST 请求
                    logger.debug("+++++++++++++++++++++++++++ workout response +++++++++++++++++++++++++++++++++++")
                    response = requests.post(url, json=payload, headers=headers)        
                    data = response.json()
                    logger.debug(data)
                    
                    
                    return JsonResponse({"status": "success"}, status=200)
                except Exception as e:
                    return {
                        'error': 'Exception',
                        'details': str(e),
                        'payload' : payload,
                        'data' : data,
                    }
            else:
                pass
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
def refresh_token(user):
    time_difference = timezone.now() - user.updated_at
    if time_difference > timedelta(hours=0):
        url = "https://wbsapi.withings.net/v2/oauth2"
        payload = {
            'action' : "requesttoken",
            'client_id' : user.client_id,
            'client_secret' : user.client_secret,
            'grant_type' : "refresh_token",
            'refresh_token' : user.refresh_token,
        }

        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload)        
            data = response.json()

            user.access_token = data['body']['access_token']
            logger.debug('+++++++++++++++ get new token +++++++++++++++++')
            logger.debug(data['body']['access_token'])
            user.save()
            
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return {
                'error': 'Exception',
                'details': str(e),
                'payload' : payload,
                'data' : data,
            }
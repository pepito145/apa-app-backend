from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserLogin, UsersInfos
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

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
    def get(request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        print(code)
        user = UserLogin.objects.get(email=state)
        user.code=code
        return Response({'code': code, 'state': state})
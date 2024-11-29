from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserLogin
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

# Inscription
class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')  # Nouveau champ
        last_name = request.data.get('last_name')  # Nouveau champ

        # Vérifie si l'email existe déjà
        if UserLogin.objects.filter(email=email).exists():
            return Response({"error": "Email déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        # Crée un nouvel utilisateur avec les champs supplémentaires
        user = UserLogin(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

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
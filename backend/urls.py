from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Fonction simple pour afficher une page d'accueil temporaire
def homepage(request):
    return HttpResponse("<h1>Bienvenue sur le serveur Django</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),  # Route pour la racine
    path('api/', include('users.urls')),  # Si tu utilises une app avec une API
]
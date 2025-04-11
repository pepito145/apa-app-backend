from django.urls import path, include
from .views import RegisterView, LoginView, Client_id, Get_code, Get_activity, get_seance, RequestActivityView,ProfileView,UpdateProfileView, Load_health_data

urlpatterns = [
    
    path('get_profil/', ProfileView.as_view(), name="get_profil"),
    path('update_profil/', UpdateProfileView.as_view(), name="update_profil"),
    path('load_health_data/', Load_health_data.as_view(), name="load_health_data"),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('client_id/', Client_id.as_view(), name='client_id'),
    path('get_code/', Get_code.as_view(), name='get_code'),
    path('get_activity/', Get_activity.as_view(), name='get_activity'),
    path('get_seance/', get_seance.as_view(), name='get_seance'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('request_activity/', RequestActivityView.as_view(), name='request_activity'),

    
]
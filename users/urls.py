from django.urls import path, include
from .views import RegisterView, LoginView, ClientID, Get_code

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('client_id/', ClientID.as_view(), name='client_id'),
    path('get_code/', Get_code.as_view(), name='get_code'),
    path('__debug__/', include('debug_toolbar.urls')),
]
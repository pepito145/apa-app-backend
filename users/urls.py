from django.urls import path, include
from .views import RegisterView, LoginView, Client_id, Get_code, Get_activity

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('client_id/', Client_id.as_view(), name='client_id'),
    path('get_code/', Get_code.as_view(), name='get_code'),
    path('get_activity/', Get_activity.as_view(), name='get_activity'),
    path('__debug__/', include('debug_toolbar.urls')),
]
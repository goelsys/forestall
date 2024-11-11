from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('core.urls')),  # Include your core app's URLs
    path('4s/', include('risk.urls')),  # Include your corerisk app's URLs
    path('supermax/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

handler404 = 'risk.views.handle_404'
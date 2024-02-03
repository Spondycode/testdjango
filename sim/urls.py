from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-in', views.SendSignInEmail.as_view(), name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('register/',views.register_blood_bank, name = 'blood_bank_register'),
    path('login/', views.custom_login_bb, name = 'login_b'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blood_bank/logout.html'), name='logout_b'),
    path('profile/', views.blood_bank_profile, name = 'profile_b'),
    # path('requests/', views.blood_bank_requests, name='blood_bank_requests'),
    path('bloodbank/update/', views.bloodbank_update, name='bloodbank_update'),
    path('update/', views.bloodbank_update, name="bloodbank_update"),
    path('delete/', views.blood_bank_delete, name='blood_bank_delete'),
    path('dashboard/', views.blood_inventory_view, name='blood_inventory'),
    path('pastreq/', views.blood_bank_dashboard, name='blood_bank_dashboard'),
]
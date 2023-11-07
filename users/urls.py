from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('',)
    path('login/', views.custom_login, name = 'login_users'),
    path('register/', views.register, name='register_user'),
    # Add more paths as needed for other views
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/',views.profile_user, name = 'profile_user'),
    path('bloodbanklist/',views.show_blood_banks, name = 'show_blood_banks'),
    path('donation_request/',views.create_donation_request, name = 'create_donation_request'),
    path('donation_success/',views.donation_success, name = 'donation_success'),
    path('request_failure/',views.request_failure, name = 'request_failure'),
    path('requestblood/',views.submit_blood_request,name = 'submit_blood_request'),
    path('user_past_requests/', views.user_past_requests, name='user_past_requests'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('request_success/<int:blood_request_id>/', views.request_success, name='request_success1'),

# ██████╗░██╗░░░░░███████╗░█████╗░░██████╗███████╗░░░░░░░░░░░░░█████╗░░█████╗░░█████╗░███████╗██████╗░████████╗
# ██╔══██╗██║░░░░░██╔════╝██╔══██╗██╔════╝██╔════╝░░░░░░░░░░░░██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
# ██████╔╝██║░░░░░█████╗░░███████║╚█████╗░█████╗░░█████╗█████╗███████║██║░░╚═╝██║░░╚═╝█████╗░░██████╔╝░░░██║░░░
# ██╔═══╝░██║░░░░░██╔══╝░░██╔══██║░╚═══██╗██╔══╝░░╚════╝╚════╝██╔══██║██║░░██╗██║░░██╗██╔══╝░░██╔═══╝░░░░██║░░░
# ██║░░░░░███████╗███████╗██║░░██║██████╔╝███████╗░░░░░░░░░░░░██║░░██║╚█████╔╝╚█████╔╝███████╗██║░░░░░░░░██║░░░
# ╚═╝░░░░░╚══════╝╚══════╝╚═╝░░╚═╝╚═════╝░╚══════╝░░░░░░░░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝╚═╝░░░░░░░░╚═╝░░░
]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             extra_context={'section': 'password-change'}
         ),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             extra_context={'section': 'password-change'}
         ),
         name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('blacklist/', views.blacklist, name='blacklist'),
    # path('push/', views.push, name='push'),
    path('profile/update-info/', views.profile_update_info, name='profile-update-info'),
    path('profile/update-price/', views.prifile_update_price, name='profile-update-price'),
    path('profile/update-services/', views.profile_update_services, name='profile-update-services'),
    path('profile/send-test-photo/', views.profile_send_test_photo, name='profile-send-test-photo'),
    path('profile/delete-test-photo/', views.profile_delete_test_photo, name='profile-delete-test-photo'),
    path('profile/send-photos/', views.profile_send_photos, name='profile-send-photos'),
    path('profile/delete-photo/', views.profile_delete_photo, name='profile-delete-photo'),
    path('profile/send-video/', views.profile_send_video, name='profile-send-video'),
    path('profile/delete-video/', views.profile_delete_video, name='profile-delete-video'),
    path('profile/check-phone/', views.profile_check_phone, name='profile-check-phone'),
    path('profile/add-phone/', views.profile_add_phone, name='profile-add-phone'),
]
from django.urls import path
from . import views

app_name = 'girls'

urlpatterns = [
    path('', views.home, name='home'),
    path('set-city/', views.city, name='city'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.catalog, name='catalog_by_slug'),
    path('search/', views.search, name='search'),
    path('by-service/<slug:slug>/', views.catalog_by_service, name='catalog_by_service'),
    path('by-real-photo/', views.catalog_real_photo, name='catalog_by_real_photo'),
    path('by-outcall/', views.catalog_outcall, name='catalog_by_outcall'),
    path('by-apartment/', views.catalog_apartment, name='catalog_by_apartment'),
    path('girl/<int:id>/', views.girl_detail, name='girl'),
    path('girl/<int:id>/add-review/', views.girl_add_review, name='add_review'),
    path('girl/<int:girl_id>/detele-review/<int:review_id>/', views.girl_delete_review, name='delete_review'),
    path('girl/<int:girl_id>/update-video-cnt/', views.girl_update_video_cnt, name='update_video_cnt'),
]
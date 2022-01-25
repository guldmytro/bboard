from django.urls import path
from . import views

app_name = 'girls'

urlpatterns = [
    path('', views.home, name='home'),
    path('girl/<int:id>/', views.girl_detail, name='girl'),
    path('girl/<int:id>/add-review/', views.girl_add_review, name='add_review'),
    path('girl/<int:girl_id>/detele-review/<int:review_id>/', views.girl_delete_review, name='delete_review'),
]
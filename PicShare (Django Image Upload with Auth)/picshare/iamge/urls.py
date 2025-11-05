from django.urls import path

from . import views

urlpatterns=[
    path('', views.upload_image, name='upload_image'),
    path('image_list/', views.image_list, name='image_list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

]
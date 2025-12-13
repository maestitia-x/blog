from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('post/<slug:slug>/', views.post, name='post'),
    path('category/<int:id>/', views.category, name='category'),
    path('profile/', views.profile, name='profile'),
]




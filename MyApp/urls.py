from django.contrib import admin
from django.urls import path
from MyApp import views

urlpatterns = [
    path('home',views.index,name='home'),
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login', views.login, name='login'),

    path('about',views.about,name='about'),
    path('contact', views.contact, name='contact'),
    path('cart', views.cart, name='cart'),
    path('logout', views.logout, name='logout'),
    path('checkout',views.checkout,name='checkout'),
    path('orders', views.orders, name='orders')


]


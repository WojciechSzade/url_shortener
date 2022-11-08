from django.urls import path

from . import views

app_name = "url"
urlpatterns = [
    path('', views.index, name='index'),
    path('shorten/<slug:slug>/', views.shorten, name='shorten'),
    path('<slug:slug>/', views.redirect_outside, name='redirect_outside'),
]
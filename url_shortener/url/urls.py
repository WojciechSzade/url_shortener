from django.urls import path
from . import views

app_name = "url"
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.redirect_outside, name='redirect_outside'),
    #TODO redirect link
   
]
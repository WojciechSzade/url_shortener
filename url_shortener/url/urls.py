from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "url"
urlpatterns = [
    path('', views.index, name='index'),
    path('shorten/<slug:slug>/', views.shorten, name='shorten'),
    path('<slug:slug>/', views.redirect_outside, name='redirect_outside'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
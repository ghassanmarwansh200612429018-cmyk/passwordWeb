"""passmannnu URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'),
    path('about/', accounts_views.about, name='about'),
    path('contact/', accounts_views.contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('vault/', include('vault.urls')),
]

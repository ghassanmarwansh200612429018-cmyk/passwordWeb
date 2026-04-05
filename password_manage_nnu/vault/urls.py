from django.urls import path
from . import views

urlpatterns = [
    path('', views.vault_dashboard, name='vault_dashboard'),
    path('add/', views.add_entry, name='add_entry'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('verify/<int:entry_id>/<str:action>/', views.verify_passkey, name='verify_passkey'),
    path('generate-password/', views.generate_password_api, name='generate_password_api'),
]

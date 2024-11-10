from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings

admin.site.site_header = "CrediScore Admin Panel"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Admin Panel"

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('submit-responses/', views.submit_responses, name='submit_responses'),
]
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.habit_list, name='habit_list'),
    path('add/', views.add_habit, name='add_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('streak/', views.streak_view, name='streak_view'),
    path('daily_scores/', views.daily_scores_view, name='daily_scores_view'),
    path('generate_tasks/', views.generate_daily_tasks, name='generate_daily_tasks'),
    path('accounts/', include('django.contrib.auth.urls')),
]
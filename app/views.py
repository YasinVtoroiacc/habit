from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from datetime import date
from .models import Habit, DailyTask, Streak, DayScore, UserHabit
from .forms import HabitForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        return reverse('habit_list')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    user_habits = UserHabit.objects.filter(user=request.user, completed_on=date.today())
    user_habit_ids = user_habits.values_list('habit_id', flat=True)

    if request.method == 'POST':
        checked_habits = request.POST.getlist('habits')
        for habit_id in checked_habits:
            habit = get_object_or_404(Habit, id=habit_id, user=request.user)
            if not UserHabit.objects.filter(user=request.user, habit=habit, completed_on=date.today()).exists():
                UserHabit.objects.create(user=request.user, habit=habit, completed_on=date.today())
                request.user.profile.points += habit.points
                request.user.profile.save()
                messages.success(request, f'Вы получили {habit.points} очков за выполнение привычки: {habit.name}')
        return redirect('habit_list')
    
    return render(request, 'habit_list.html', {'habits': habits, 'user_habit_ids': user_habit_ids})

@login_required
def daily_scores_view(request):
    scores = DayScore.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'daily_scores_view.html', {
        'scores': scores,
    })

@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Привычка успешно добавлена!')
            return redirect('habit_list')
    else:
        form = HabitForm()
    
    return render(request, 'add_habit.html', {'form': form})

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    messages.success(request, 'Привычка удалена!')
    return redirect('habit_list')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(DailyTask, id=task_id, habit__user=request.user)
    
    if not task.completed:
        task.complete_task()
        today = timezone.now().date()
        day_score, created = DayScore.objects.get_or_create(user=request.user, date=today)
        day_score.points += task.habit.points
        day_score.save()

        streak, created = Streak.objects.get_or_create(user=request.user)
        streak.update_streak()

        messages.success(request, f'Задача "{task.habit.name}" выполнена! Очки добавлены.')
    return redirect('habit_list')

@login_required
def streak_view(request):
    streak, created = Streak.objects.get_or_create(user=request.user)
    
    return render(request, 'streak_view.html', {
        'longest_streak': streak.longest_streak,
        'current_streak': streak.current_streak,
    })

@login_required
def generate_daily_tasks(request):
    today = timezone.now().date()
    habits = Habit.objects.filter(user=request.user)
    
    for habit in habits:
        DailyTask.objects.get_or_create(habit=habit, date=today)

    messages.info(request, 'Ежедневные задачи успешно созданы (если они еще не были).')
    return redirect('habit_list')
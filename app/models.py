from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
    if created:
        # Создание профиля только если он не существует
        Profile.objects.get_or_create(user=instance)
    else:
        # Если профиль уже существует, просто сохраняем его
        instance.profile.save()
   
    
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserHabit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    completed_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.habit.name}'

class DailyTask(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['habit', 'date']

    def complete_task(self):
        self.completed = True
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.habit.name} - {self.date}"

class Streak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_completed_date = models.DateField(null=True, blank=True)

    def update_streak(self):
        today = timezone.now().date()
        if self.last_completed_date == today - timezone.timedelta(days=1):
            self.current_streak += 1
        else:
            self.current_streak = 1
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        self.last_completed_date = today
        self.save()

    def __str__(self):
        return f"{self.user.username} - Current Streak: {self.current_streak}, Longest Streak: {self.longest_streak}"

class DayScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.points} points"
  



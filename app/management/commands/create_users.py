from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile

class Command(BaseCommand):
    help = 'Создает пользователей с профилями'

    def handle(self, *args, **kwargs):
        # Данные для новых пользователей
        users_data = [
            {'username': 'Иман.', 'password': 'password1'},
            {'username': 'Ясин.', 'password': 'password2'},
            {'username': 'Илим.', 'password': 'password3'},
            {'username': 'Ислам.', 'password': 'password4'},
            {'username': 'Амак.', 'password': 'password5'},  # Амиджан (Амак)
        ]

        # Создание пользователей и профилей
        for user_data in users_data:
            user, created = User.objects.get_or_create(username=user_data['username'])

            # Если пользователь только что создан (created == True), задаем пароль
            if created:
                user.set_password(user_data['password'])
                user.save()

            # Создание профиля, если он не существует
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)

            self.stdout.write(self.style.SUCCESS(f"Пользователь {user.username} создан с профилем."))

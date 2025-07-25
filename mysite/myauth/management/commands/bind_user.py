# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User, Group, Permission

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         user = User.objects.get(pk=1)
#         group, created = Group.objects.get_or_create(
#             name='profile_manager',
#         )
#         permission = Permission.objects.get(
#             codename='view_profile',
#         )
#         permission_logentry = Permission.objects.get(
#             codename='view_logentry',
#         )

#         group.permissions.add(permission)

#         user.groups.add(group)
#         user.user_permissions.add(permission_logentry)
#         group.save()
#         user.save()

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Получаем пользователя
        user = User.objects.get(pk=2)
        
        # Создаем или получаем группу
        group, created = Group.objects.get_or_create(
            name='profile_manager',
        )
        
        # Получаем разрешения
        permission = Permission.objects.get(
            codename='view_profile',
        )
        permission_logentry = Permission.objects.get(
            codename='view_logentry',
        )

        # Добавляем разрешения в группу
        group.permissions.add(permission)  
        
        # Назначаем группу и разрешения пользователю
        user.groups.add(group)
        user.user_permissions.add(permission_logentry)
        
        # Сохраняем изменения
        group.save()
        user.save()
        
        self.stdout.write(self.style.SUCCESS('Права успешно назначены!'))
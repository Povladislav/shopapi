from django.contrib.auth.models import User
from rest_framework import permissions

"""
Для удобства я буду сразу прокидывать моего суперюзера,
хотя если бы у нас было их много и реализована полноценная регистрация/авторизация,
мы бы использовали строчку, которю я закомментил для проверки, является ли юзер активным.
"""


class IsActiveUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = User.objects.first()
        # user = request.user

        return user.is_authenticated and user.is_active

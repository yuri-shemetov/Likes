from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like, Report

User = get_user_model()

def add_like(obj, user):
    """Лайкает `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like

def remove_like(obj, user):
    """Удаляет лайк с `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()

def is_fan(obj, user):
    """Проверяет, лайкнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()
    
def get_fans(obj):
    """Получает всех пользователей, которые лайкнули `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)

def add_report(obj, user):
    """Делает репорт `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    report, is_created = Report.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return report

def remove_report(obj, user):
    """Удаляет репорт с `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Report.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()

def is_report(obj, user):
    """Проверяет, сделал ли `user` репорт `obj`.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    reports = Report.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return reports.exists()
    
def get_reports(obj):
    """Получает всех пользователей, которые сделали репорт `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        reports__content_type=obj_type, reports__object_id=obj.id)
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаёт группу Модератор продуктов"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Модератор продуктов"
        )

        can_unpublish_permission = Permission.objects.get(
            codename="can_unpublish_product",
            content_type__app_label="catalog",
            content_type__model="product",
        )

        delete_permission = Permission.objects.get(
            codename="delete_product",
            content_type__app_label="catalog",
            content_type__model="product",
        )

        group.permissions.set(
            [
                can_unpublish_permission,
                delete_permission,
            ]
        )

        if created:
            message = "Группа 'Модератор продуктов' создана"
        else:
            message = "Группа 'Модератор продуктов' обновлена"

        self.stdout.write(self.style.SUCCESS(message))

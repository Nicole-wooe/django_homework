from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Load products and categories from fixtures'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command('loaddata', 'fixtures/categories.json')
        call_command('loaddata', 'fixtures/products.json')

        self.stdout.write(
            self.style.SUCCESS('Данные успешно загружены')
        )

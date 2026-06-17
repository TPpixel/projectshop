from django.core.management import BaseCommand, call_command
from shopapp.models import Product

class Command(BaseCommand):
    help = 'Load seed data from data.json if no products exist'

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists, skipping'))
            return
        call_command('loaddata', 'data.json')
        self.stdout.write(self.style.SUCCESS('Seed data loaded'))

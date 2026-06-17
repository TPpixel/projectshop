from django.core.management import BaseCommand, call_command

class Command(BaseCommand):
    help = 'Load seed data from data.json if no products exist'

    def handle(self, *args, **options):
        from django.db import connection
        from django.db.utils import OperationalError

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM shopapp_product")
            count = cursor.fetchone()[0]
            if count > 0:
                self.stdout.write(self.style.WARNING('Data already exists, skipping'))
                return
        except OperationalError:
            self.stdout.write(self.style.WARNING('Tables not ready yet, skipping'))

        try:
            call_command('loaddata', 'data.json', verbosity=0)
            self.stdout.write(self.style.SUCCESS('Seed data loaded'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Seed data skipped: {e}'))

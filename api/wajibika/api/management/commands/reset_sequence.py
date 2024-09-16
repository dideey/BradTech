# your_app/management/commands/reset_sequence.py
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Resets the auto-increment sequence for the specified table'

    def add_arguments(self, parser):
        parser.add_argument('table_name', type=str, help='The name of the table to reset the sequence for')

    def handle(self, *args, **kwargs):
        table_name = kwargs['table_name']
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute(f'ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;')
            elif connection.vendor == 'mysql':
                cursor.execute(f'ALTER TABLE {table_name} AUTO_INCREMENT = 1;')
            elif connection.vendor == 'sqlite':
                cursor.execute(f'UPDATE sqlite_sequence SET seq = 0 WHERE name = "{table_name}";')
            else:
                self.stdout.write(self.style.ERROR('Unsupported database vendor'))
                return
        self.stdout.write(self.style.SUCCESS(f'Successfully reset sequence for table {table_name}'))
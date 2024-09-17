import json
import os
from django.core.management.base import BaseCommand
from api.models import Leaders, Ward

class Command(BaseCommand):
    help = 'Import mcas data from JSON file into the Leaders model'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']

        # Check if the file exists
        if not os.path.isfile(json_file_path):
            self.stderr.write(f"File {json_file_path} does not exist.")
            return

        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Loop through the data and create Leaders
        for ward_code, mca_name in data.items():
            # Get the County instance based on county code
            try:
                ward = Ward.objects.get(id=ward_code)
            except Ward.DoesNotExist:
                self.stderr.write(f"Ward  with code {ward_code} does not exist.")
                continue

            # Create or update the Leader instance
            Leaders.objects.update_or_create(
                name=mca_name,
                defaults={
                    'position': 'member of county assembly',
                    'ward': ward,
                    'image': '',
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported mcas.'))

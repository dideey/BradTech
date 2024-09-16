import json
import os
from django.core.management.base import BaseCommand
from api.models import Leaders, County

class Command(BaseCommand):
    help = 'Import womenrep data from JSON file into the Leaders model'

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
        for county_code, womenrep_name in data.items():
            # Get the County instance based on county code
            try:
                county = County.objects.get(id=county_code)
            except County.DoesNotExist:
                self.stderr.write(f"County with code {county_code} does not exist.")
                continue

            # Create or update the Leader instance
            Leaders.objects.update_or_create(
                name=womenrep_name,
                defaults={
                    'position': 'women representative',
                    'county': county,
                    'image': '',
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported womenreps.'))

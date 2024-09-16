import json
from django.core.management.base import BaseCommand
from api.models import County, Constituency

class Command(BaseCommand):
    help = 'Load constituencies and link them to counties'

    def handle(self, *args, **kwargs):
        # Load JSON data
        with open('/home/outlaw/Downloads/constituencies.json', 'r') as f:
            constituencies_data = json.load(f)

        # Process each constituency
        for constituency in constituencies_data:
            constituency_name = constituency['name']
            constituency_code = constituency['code']
            county_code = constituency['county_code']

            try:
                # Find the matching county by county_code
                county = County.objects.get(id=county_code)
                
                # Create the constituency linked to the county
                Constituency.objects.create(name=constituency_name, id=constituency_code, county=county)
                self.stdout.write(self.style.SUCCESS(f"Successfully added {constituency_name} linked to {county.name}"))
            
            except County.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"County with code {county_code} not found"))
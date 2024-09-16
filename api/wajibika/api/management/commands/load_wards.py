import json
from django.core.management.base import BaseCommand
from api.models import Constituency, Ward  

class Command(BaseCommand):
    help = 'Load wards and link them to constituencies'

    def handle(self, *args, **kwargs):
        # Load JSON data
        with open('/home/outlaw/Downloads/wards.json', 'r') as f:
            wards_data = json.load(f)

        # Process each ward
        for ward in wards_data:
            ward_name = ward['name']
            ward_code = ward['code']
            constituency_code = ward['constituency_code']

            try:
                # Find the matching constituency by constituency_code
                constituency = Constituency.objects.get(id=constituency_code)
                
                # Create the ward linked to the constituency
                Ward.objects.create(name=ward_name, id=ward_code, constituency=constituency)
                self.stdout.write(self.style.SUCCESS(f"Successfully added {ward_name} linked to {constituency.name}"))
            
            except Constituency.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Constituency with code {constituency_code} not found"))

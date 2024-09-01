import pandas as pd
from django.core.management.base import BaseCommand
from main.models import City, Region

class Command(BaseCommand):
    help = 'Import cities from an Excel file into the database'

    def handle(self, *args, **kwargs):
        # Зчитування даних з Excel файлу
        excel_data = pd.read_excel('cities.xlsx')

        for _, row in excel_data.iterrows():
            region_name = row['region']
            region, created = Region.objects.get_or_create(name=region_name)
            city, created = City.objects.get_or_create(
                name=row['name'],
                region=region,
                latitude=row['latitude'],
                longitude=row['longitude']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added city: {row['name']} in region {region_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"City already exists: {row['name']} in region {region_name}"))
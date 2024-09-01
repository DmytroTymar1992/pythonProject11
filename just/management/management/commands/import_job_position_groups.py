# management/management/commands/import_job_position_groups.py

import pandas as pd
from django.core.management.base import BaseCommand
from company.models import JobPositionGroup
import os

class Command(BaseCommand):
    help = 'Import job position groups from an Excel file into the database'

    def handle(self, *args, **kwargs):
        # Зчитування даних з Excel файлу
        file_path = os.path.join('job_position_groups.xlsx')
        excel_data = pd.read_excel(file_path)

        for _, row in excel_data.iterrows():
            group_name = row['name']
            group, created = JobPositionGroup.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added job position group: {group_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Job position group already exists: {group_name}"))

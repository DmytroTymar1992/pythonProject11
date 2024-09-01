# management/management/commands/import_job_categories.py

import pandas as pd
from django.core.management.base import BaseCommand
from company.models import JobCategory
import os
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import job categories from an Excel file into the database'

    def handle(self, *args, **kwargs):
        # Зчитування даних з Excel файлу
        file_path = os.path.join('job_categories.xlsx')
        excel_data = pd.read_excel(file_path)

        for _, row in excel_data.iterrows():
            category_name = row['name']
            slug = slugify(category_name)

            # Перевірка унікальності slug і додавання суфікса, якщо він вже існує
            unique_slug = slug
            counter = 1
            while JobCategory.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{slug}-{counter}'
                counter += 1

            category, created = JobCategory.objects.get_or_create(name=category_name, defaults={'slug': unique_slug})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added job category: {category_name} with slug {unique_slug}"))
            else:
                self.stdout.write(self.style.WARNING(f"Job category already exists: {category_name}"))

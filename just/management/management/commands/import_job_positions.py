# management/management/commands/import_job_positions.py

import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from company.models import JobPosition, JobCategory, JobPositionGroup
import os

class Command(BaseCommand):
    help = 'Import job positions from an Excel file into the database'

    def handle(self, *args, **kwargs):
        # Зчитування даних з Excel файлу
        file_path = os.path.join('job_positions.xlsx')
        excel_data = pd.read_excel(file_path)

        for _, row in excel_data.iterrows():
            position_name = row['укр']
            group_name = row['Група']

            # Збирання всіх категорій з різних колонок в один список
            category_names = [row[col].strip() for col in ['Категорія', 'Категорія', 'Категорія'] if pd.notna(row[col])]

            # Генерація унікального slug
            slug = slugify(position_name)
            unique_slug = slug
            counter = 1
            while JobPosition.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{slug}-{counter}'
                counter += 1

            # Створення або отримання позиції
            position, created = JobPosition.objects.get_or_create(name=position_name, slug=unique_slug, defaults={'name_ru': ''})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added job position: {position_name} with slug {unique_slug}"))
            else:
                self.stdout.write(self.style.WARNING(f"Job position already exists: {position_name}"))

            # Створення або отримання груп та додавання до позиції
            if pd.notna(group_name):
                group_name = group_name.strip()
                group, _ = JobPositionGroup.objects.get_or_create(name=group_name)
                position.groups.add(group)

            # Створення або отримання категорій та додавання до позиції
            for category_name in category_names:
                category, _ = JobCategory.objects.get_or_create(name=category_name)
                position.categories.add(category)

            position.save()

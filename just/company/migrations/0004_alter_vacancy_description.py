# Generated by Django 4.2.13 on 2024-08-29 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_alter_vacancy_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.TextField(verbose_name='Опис'),
        ),
    ]

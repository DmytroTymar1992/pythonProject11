# Generated by Django 4.2.13 on 2024-08-25 20:53

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Опис'),
        ),
    ]

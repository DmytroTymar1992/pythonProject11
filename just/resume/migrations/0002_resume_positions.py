# Generated by Django 4.2.13 on 2024-07-28 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='positions',
            field=models.CharField(default='Вантажник', max_length=255),
        ),
    ]

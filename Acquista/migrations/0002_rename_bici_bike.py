# Generated by Django 4.2.2 on 2023-06-18 14:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Acquista', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='bici',
            new_name='Bike',
        ),
    ]

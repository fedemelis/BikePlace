# Generated by Django 4.2.2 on 2023-06-23 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Acquista', '0016_bikecomponent_compositebike'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikecomponent',
            name='vendor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='component_vendor', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
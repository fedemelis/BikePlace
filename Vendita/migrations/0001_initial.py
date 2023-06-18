# Generated by Django 4.2.2 on 2023-06-18 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='bici',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_bike', models.CharField(choices=[('Bici da strada', 'Bici da Strada'), ('Bici da montagna', 'Bici da Montagna'), ('Bici da città', 'Bici da Città'), ('Bici ibride', 'Bici Ibride'), ('Bici da corsa', 'Bici da Corsa'), ('Bici da cicloturismo', 'Bici da Cicloturismo'), ('Bici da gravel', 'Bici da Gravel'), ('Bici da pista', 'Bici da Pista'), ('Bici BMX', 'Bici BMX'), ('Bici pieghevoli', 'Bici Pieghevoli')], max_length=20)),
                ('brand', models.CharField(max_length=50)),
                ('year_of_production', models.IntegerField()),
                ('price', models.IntegerField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bici', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

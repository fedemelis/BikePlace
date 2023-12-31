# Generated by Django 4.2.2 on 2023-06-21 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Acquista', '0009_soldbike_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'Ordini'},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ordered_at',
            new_name='order_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='sold_bike',
        ),
        migrations.AddField(
            model_name='order',
            name='sold_bikes',
            field=models.ManyToManyField(related_name='orders', to='Acquista.soldbike'),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-17 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmenu',
            name='food_image',
            field=models.CharField(),
        ),
    ]

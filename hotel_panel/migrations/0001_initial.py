# Generated by Django 4.2.6 on 2023-12-05 06:40

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HotelOwner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("contact", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "id_proof",
                    models.FileField(blank=True, null=True, upload_to="owner_id"),
                ),
                ("id_number", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="hotelowner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HotelsAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hotel_name", models.CharField(max_length=255)),
                (
                    "profile_photo",
                    models.FileField(blank=True, null=True, upload_to="hotel_profile"),
                ),
                ("description", models.TextField()),
                ("contact", models.CharField(max_length=100)),
                ("alt_contact", models.CharField(max_length=100)),
                ("certificate", models.FileField(upload_to="hotel_certificate")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("address", models.TextField()),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                ("rating", models.FloatField(blank=True, default=0.0, null=True)),
                ("is_active", models.BooleanField(default=False)),
                ("is_logined", models.BooleanField(default=False)),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="hotelaccount",
                        to="hotel_panel.hotelowner",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FoodMenu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("food_name", models.CharField(max_length=255)),
                ("food_type", models.CharField(max_length=255)),
                ("food_image", models.CharField()),
                ("food_price", models.FloatField()),
                ("offer_price", models.FloatField(blank=True, null=True)),
                ("description", models.TextField()),
                ("is_veg", models.BooleanField(default=False)),
                ("is_available", models.BooleanField(default=False)),
                (
                    "hotel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="foodmenu",
                        to="hotel_panel.hotelsaccount",
                    ),
                ),
            ],
        ),
    ]

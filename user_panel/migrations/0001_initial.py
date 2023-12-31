# Generated by Django 4.2.6 on 2023-12-05 06:40

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hotel_panel", "0001_initial"),
        ("delivery_boy", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Shopping",
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
                (
                    "del_location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, db_index=True, null=True, srid=4326
                    ),
                ),
                ("address", models.TextField(blank=True, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("quantity", models.IntegerField()),
                ("total_amount", models.FloatField()),
                ("is_canceled", models.BooleanField(default=False)),
                ("is_completed", models.BooleanField(default=False)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="hotel_panel.foodmenu",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ShoppingDeliveryPerson",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ordered", "Ordered"),
                            ("purchasing", "Purchasing"),
                            ("on_the_way", "On The Way"),
                            ("delivered", "Delivered"),
                            ("canceled", "Canceled"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "delivery_person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="delivery_boy.deliveryperson",
                    ),
                ),
                (
                    "shopping",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="user_panel.shopping",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeliveryNotification",
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
                (
                    "status",
                    models.CharField(
                        choices=[("accepted", "Accepted"), ("rejected", "Rejected")],
                        max_length=20,
                    ),
                ),
                (
                    "delivery_person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="delivery_boy.deliveryperson",
                    ),
                ),
                (
                    "shopping",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="user_panel.shopping",
                    ),
                ),
            ],
        ),
    ]

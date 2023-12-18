# Generated by Django 4.2.6 on 2023-12-18 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user_panel", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShoppingPayment",
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
                ("stripe_id", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="shopping",
            name="payment_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="user_panel.shoppingpayment",
            ),
        ),
    ]

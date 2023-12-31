# Generated by Django 4.2.6 on 2023-12-30 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user_panel", "0008_shoppingpayment_hotel_loc"),
        ("chat", "0003_alter_message_receiver"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="order_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="user_panel.shoppingpayment",
            ),
        ),
    ]

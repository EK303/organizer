# Generated by Django 4.1.3 on 2022-12-01 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_card_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="main.card",
            ),
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-01 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_alter_card_due_date"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="card",
            unique_together={("title", "column")},
        ),
    ]

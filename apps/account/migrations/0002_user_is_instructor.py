# Generated by Django 5.1.6 on 2025-03-05 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_instructor',
            field=models.BooleanField(default=False),
        ),
    ]

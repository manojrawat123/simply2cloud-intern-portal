# Generated by Django 4.0.3 on 2024-02-01 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internuser',
            name='phone',
            field=models.IntegerField(unique=True),
        ),
    ]

# Generated by Django 4.0.3 on 2024-02-02 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern_user', '0007_alter_internuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internuser',
            name='user_type',
            field=models.CharField(max_length=225),
        ),
    ]

# Generated by Django 4.0.3 on 2024-02-02 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern_user', '0002_alter_internuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='internuser',
            name='user_type',
            field=models.CharField(choices=[('user', 'user'), ('company_user', 'company_user')], default='user', max_length=225),
        ),
        migrations.AlterField(
            model_name='internuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
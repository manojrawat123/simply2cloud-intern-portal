# Generated by Django 4.0.3 on 2024-02-02 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern_user', '0003_internuser_user_type_alter_internuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internuser',
            name='user_type',
            field=models.CharField(choices=[('user', 'user'), ('company_user', 'company_user')], max_length=225),
        ),
    ]

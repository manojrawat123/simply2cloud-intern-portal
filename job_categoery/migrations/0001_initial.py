# Generated by Django 4.0.3 on 2024-02-13 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_category', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('display', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Job Categories',
            },
        ),
    ]
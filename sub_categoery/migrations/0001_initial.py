# Generated by Django 4.0.3 on 2024-02-13 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job_categoery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_display', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_categoery.jobcategory')),
            ],
        ),
    ]
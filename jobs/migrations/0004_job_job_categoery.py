# Generated by Django 4.0.3 on 2024-02-07 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_categoery', '0002_jobcategory_display'),
        ('jobs', '0003_alter_job_company_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_categoery',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='job_categoery.jobcategory'),
        ),
    ]

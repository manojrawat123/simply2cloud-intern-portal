# Generated by Django 4.0.3 on 2024-02-07 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_categoery', '0002_jobcategory_display'),
        ('intern_job_profile', '0002_alter_internjobprofile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='internjobprofile',
            name='job_categoery',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='job_categoery.jobcategory'),
        ),
    ]

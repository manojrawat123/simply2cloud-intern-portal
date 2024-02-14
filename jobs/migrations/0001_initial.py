# Generated by Django 4.0.3 on 2024-02-13 07:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
        ('available_skills', '0001_initial'),
        ('sub_categoery', '0001_initial'),
        ('job_categoery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('experience', models.CharField(max_length=255)),
                ('education', models.CharField(max_length=255)),
                ('student_hired', models.IntegerField(default=0)),
                ('location', models.CharField(max_length=255)),
                ('job_commute_type', models.CharField(choices=[('remote', 'remote'), ('work_from_home', 'work_from_home'), ('both', 'both')], max_length=50)),
                ('timezone_required', models.CharField(max_length=255)),
                ('responsibilities', models.TextField(blank=True, null=True)),
                ('qualifications', models.TextField(blank=True, null=True)),
                ('benefits', models.TextField(blank=True, null=True)),
                ('application_deadline', models.DateField(blank=True, null=True)),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('company_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job_categoery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_categoery.jobcategory')),
                ('skills_preferred', models.ManyToManyField(related_name='skills_preffered', to='available_skills.availableskill')),
                ('skills_required', models.ManyToManyField(related_name='skills_required', to='available_skills.availableskill')),
                ('sub_categoery', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sub_categoery.subcategory')),
            ],
        ),
    ]

# Generated by Django 4.0.3 on 2024-02-13 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0003_alter_skill_skill_id'),
        ('available_skills', '0001_initial'),
        ('intern_profile_job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internjobprofile',
            name='available_skills',
            field=models.ManyToManyField(to='available_skills.availableskill'),
        ),
        migrations.AlterField(
            model_name='internjobprofile',
            name='skills',
            field=models.ManyToManyField(to='skills.skill'),
        ),
    ]

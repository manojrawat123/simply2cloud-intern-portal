from django.db import models

class AvailableSkill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=225,  choices=[
        ("Web Devlopment", "Web Devlopment"),
        ("App Devlopment", "App Devlopment"),
        ("MERN Stack", "MERN Stack"),
        ("Graphic Designer", "Graphic Designer"),
        ("Video Editor", "Video Editor")
    ])
    def __str__(self):
        return self.name
    
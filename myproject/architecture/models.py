import os

from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


class Architect(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ArchitectureProject(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    year = models.IntegerField(blank=True, null=True)
    adress = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    country = CountryField()
    architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    project_category = models.ManyToManyField(ProjectCategory)
    user_likes = models.ManyToManyField(User, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_by')

    def __str__(self):
        return self.name


def content_file_name(instance, filename):
    return os.path.join(str(instance.architecture_project.pk), filename)


class Photo(models.Model):
    PHOTO_TYPE = (
        (1, 'photo'),
        (2, 'minimap'),
        (3, 'schema'),
        (4, 'drawing'),
        (5, 'other'),
    )

    category = models.IntegerField(choices=PHOTO_TYPE)
    architecture_project = models.ForeignKey(ArchitectureProject, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.ImageField(upload_to=content_file_name)
    title = models.BooleanField(default=False)

    def __str__(self):
        return self.path.url


class UserProfile(models.Model):
    """extension of user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()

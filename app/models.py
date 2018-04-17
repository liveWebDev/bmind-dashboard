"""
Definition of models.
"""
import pandas as pd
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from DataViz.settings import DATA_ROOT


# extends User Class to our own attributes in an One to One relationship - Leandro
class UserProfileInfo(models.Model):
    # Create relationship One to One
    user = models.OneToOneField(User, models.PROTECT)

    # Add additional attributes
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        # Bult-in attribute of django.contrib.auth.models.User
        return self.user.username


class CatalogItem(models.Model):
    name = models.CharField(max_length=30)
    fato = models.IntegerField

    def load(self):
        df = pd.read_csv(DATA_ROOT + '/data.csv')

        self.objects.bulk_create(
            self(**vals) for vals in df.to_dict('records')
        )

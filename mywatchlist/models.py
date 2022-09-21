from django.db import models


# Create your models here.
class WatchList(models.Model):
    watched = models.BooleanField()
    title = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    release_date = models.CharField(max_length=55)
    review = models.TextField()

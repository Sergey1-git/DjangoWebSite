from django.db import models

class BasketModel(models.Model):
    objects = models.Manager()
    id_users = models.CharField(max_length=255)
    dict_order=models.CharField(max_length=255)
    cost = models.FloatField()
    address=models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

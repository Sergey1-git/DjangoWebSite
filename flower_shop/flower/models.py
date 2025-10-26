from django.db import models

class Flower(models.Model):


    objects = models.Manager()
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    plant_type=models.CharField(max_length=255, blank=False)
    price=models.FloatField()
    quantity=models.IntegerField()
    photo = models.ImageField(upload_to="photos/%Y.%m.%d/", default=None, null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

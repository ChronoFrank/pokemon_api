from django.db import models

# Create your models here.

class Pokemon(models.Model):
    pokemon_id = models.IntegerField()
    name = models.CharField(max_length=200)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    evolution = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

class BaseStat(models.Model):
    name = models.CharField(max_length=25)
    base_stat = models.IntegerField(default=0)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True, blank=True)
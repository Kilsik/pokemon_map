from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)


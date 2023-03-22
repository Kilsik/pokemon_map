from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null=True, blank=True)
    title_jp = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='pokemons', null=True)
    description = models.TextField(null=True, blank=True)
    previous_evolution = models.ForeignKey('self', null=True, blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField('Lat')
    lon = models.FloatField('Lon')
    appeared_at = models.DateTimeField('Appeared at', null=True)
    disappeared_at = models.DateTimeField('Disappeared at', null=True)
    level = models.IntegerField('Level', null=True)
    health = models.IntegerField('Health', null=True)
    strength = models.IntegerField('Strength', null=True)
    defence = models.IntegerField('Defence', null=True)
    stamina = models.IntegerField('Stamina', null=True)

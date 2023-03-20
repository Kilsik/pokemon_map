from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemons', null=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField('Lat')
    lon = models.FloatField('Lot')
    appeared_at = models.DateTimeField('Appeared at', null=True)
    disappeared_at = models.DateTimeField('Disappeared at', null=True)

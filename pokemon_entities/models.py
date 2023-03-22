from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200, null=True, blank=True,
        verbose_name='Англ.название')
    title_jp = models.CharField(max_length=200, null=True, blank=True,
        verbose_name='Яп.название')
    image = models.ImageField(upload_to='pokemons', null=True,
        verbose_name='Внешность')
    description = models.TextField(null=True, blank=True,
        verbose_name='Описание')
    previous_evolution = models.ForeignKey('self',
        verbose_name='Из кого эволюционирует', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='next_evolution')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появился', null=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчез', null=True)
    level = models.IntegerField(verbose_name='Уровень', null=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True)
    strength = models.IntegerField(verbose_name='Атака', null=True)
    defence = models.IntegerField(verbose_name='Защита', null=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True)

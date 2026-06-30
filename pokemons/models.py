from django.contrib.auth.models import User
from django.db import models


class Pokemon(models.Model):
    pokemon_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=500, null=True, blank=True)
    types = models.CharField(max_length=200, null=True, blank=True)
    abilities = models.CharField(max_length=200, null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class FavoritePokemon(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    pokemon_obj = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        null=True,
        blank=True,
    )
    pokemon_id = models.IntegerField()
    pokemon_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "pokemon_id")

    def __str__(self):
        return f"{self.user.username} loves {self.pokemon_name}"
from django.contrib.auth.models import User
from django.db import models

from favamealapi.models.favoriterestaurant import FavoriteRestaurant


class Restaurant(models.Model):

    name = models.CharField(max_length=55, unique=True)
    address = models.CharField(max_length=255)
    favorites = models.ManyToManyField(User, through="FavoriteRestaurant")
    # TODO: Add a `favorite` custom property
    @property
    def favorite(self):
        return self.__favorite
    @favorite.setter
    def favorite(self, user):
        try:
            favorites = FavoriteRestaurant.objects.get(restaurant= self, user = user)
            if favorites:
                self.__favorite = True
        except:
            self.__favorite = False
        
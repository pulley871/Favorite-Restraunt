from django.db import models
from django.contrib.auth.models import User

from favamealapi.models.mealrating import MealRating


class Meal(models.Model):

    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, through="FavoriteMeal")
   
    # TODO: Add an user_rating custom properties

    # TODO: Add an avg_rating custom properties
    @property
    def avg_rating(self):
        """"Gets the average rating for meals"""
        ratings = MealRating.objects.filter(meal=self)
        if len(ratings) == 0:
            return "This meal has no ratings"
        else:
            average = 0
            for rating in ratings:
                average += rating.rating
            return average /len(ratings)
   
    def user_rating(self, user):
        ''''Gets the users rating for the meal'''
        ratings = MealRating.objects.filter(meal=self)
        for rating in ratings:
            if rating.user == user:
                return rating.rating
            else:
                return "User has not rated yet"
    @property
    def is_favorite(self):
        return self.__is_favorite
    @is_favorite.setter
    def is_favorite(self, value):
        if value:
            self.__is_favorite = True
        else:
            self.__is_favorite = False
       
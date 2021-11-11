"""View module for handling requests about meals"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from favamealapi.models import Meal, MealRating, Restaurant, FavoriteMeal
from favamealapi.views.restaurant import RestaurantSerializer
from django.contrib.auth.models import User

class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals"""
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'restaurant', 'user_rating', 'avg_rating', 'is_favorite')


class MealView(ViewSet):
    """ViewSet for handling meal requests"""

    def create(self, request):
        """Handle POST operations for meals

        Returns:
            Response -- JSON serialized meal instance
        """
        meal = Meal()
        meal.name = request.data["name"]
        meal.restaurant = Restaurant.objects.get(pk=request.data["restaurant_id"])


        try:
            meal.save()
            serializer = MealSerializer(
                meal, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single meal

        Returns:
            Response -- JSON serialized meal instance
        """
        try:
            meal = Meal.objects.get(pk=pk)

            # TODO: Get the rating for current user and assign to `user_rating` property

            # TODO: Get the average rating for requested meal and assign to `avg_rating` property

            # TODO: Assign a value to the `is_favorite` property of requested meal


            serializer = RestaurantSerializer(
                meal, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to meals resource

        Returns:
            Response -- JSON serialized list of meals
        """
        user = request.auth.user
        meals = Meal.objects.all()
        for meal in meals:
            meal.user_rating = meal.user_rating(user)
            meal.restaurant.favorite = user
            favorite_meal = FavoriteMeal.objects.filter(user = user, meal = meal)
            meal.is_favorite = favorite_meal

        # TODO: Get the rating for current user and assign to `user_rating` property
        
        # TODO: Get the average rating for each meal and assign to `avg_rating` property

        # TODO: Assign a value to the `is_favorite` property of each meal

        serializer = MealSerializer(
            meals, many=True, context={'request': request})

        return Response(serializer.data)

    # TODO: Add a custom action named `rate` that will allow a client to send a
    #  POST and a PUT request to /meals/3/rate with a body of..
    #       {
    #           "rating": 3
    #       }
    @action(methods=['post','delete'], detail=True)
    def rate(self,request, pk=None):
        '''Handles Posting to favorites'''
        user = request.auth.user
        try:
            meal = Meal.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({'message': 'Meal does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            try:
                MealRating.objects.create(
                    user = user,
                    meal = meal,
                    rating = request.data["rating"]
                )
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({"message": ex.args[0]})
        if request.method == "DELETE":
            try:
                user_rating = MealRating.objects.get(user=user , meal=meal)
                user_rating.delete()
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({"message": ex.args[0]})

    @action(methods=['post','delete'], detail=True)
    def star(self,request, pk=None):
        '''Handles Posting to favorites'''
        user = request.auth.user
        try:
            meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response({'message': 'Meal does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            try:
                meal.favorites.add(user)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({"message": ex.args[0]})
        if request.method == "DELETE":
            try:
                meal.favorites.remove(user)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({"message": ex.args[0]})

    # TODO: Add a custom action named `star` that will allow a client to send a
    #  POST and a DELETE request to /meals/3/star.

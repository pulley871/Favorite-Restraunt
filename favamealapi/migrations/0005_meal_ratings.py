# Generated by Django 3.2.9 on 2021-11-11 19:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('favamealapi', '0004_meal_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='ratings',
            field=models.ManyToManyField(related_name='rated_meals', through='favamealapi.MealRating', to=settings.AUTH_USER_MODEL),
        ),
    ]

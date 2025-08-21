from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=255)
    cooking_time = models.IntegerField()
    # blank=True allow the field to be empty and then autofilled
    difficulty = models.CharField(max_length=25, blank=True)
    description = models.TextField()
    # come back to define "upload_to"
    pic = models.ImageField(upload_to='', default='no_picture.jpg')

    def __str__(self):
        return str(self.name)

     # calculates the difficulty of each recipe based on cooking time and number of ingredients
    def calculate_difficulty(self):
        ingredients = self.return_ingredients_as_list()
        if self.cooking_time < 10 and len(ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            self.difficulty = 'Hard'
        return self.difficulty

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        else:
            ingredients_list = [ingredient.strip()
                                for ingredient in self.ingredients.split(', ')]
            return ingredients_list

    def save(self, *args, **kwargs):
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipeApp:detail', kwargs={'pk': self.pk})

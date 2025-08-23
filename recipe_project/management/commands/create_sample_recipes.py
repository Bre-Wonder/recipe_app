from django.core.management.base import BaseCommand
from recipeApp.models import Recipe
import os

class Command(BaseCommand):
    help = 'Create sample recipes with images for testing'

    def handle(self, *args, **options):
        # Sample recipes with their corresponding image files
        sample_recipes = [
            {
                'name': 'Sourdough Bread',
                'ingredients': 'flour, water, salt, sourdough starter',
                'cooking_time': 24,
                'description': 'A classic sourdough bread with a tangy flavor and crispy crust.',
                'pic': 'sourdough.jpg'
            },
            {
                'name': 'Lasagna',
                'ingredients': 'pasta sheets, ground beef, ricotta cheese, mozzarella, tomato sauce',
                'cooking_time': 90,
                'description': 'Layered pasta dish with rich meat sauce and melted cheese.',
                'pic': 'lasagna.jpg'
            },
            {
                'name': 'Blueberry Smoothie',
                'ingredients': 'blueberries, yogurt, honey, ice',
                'cooking_time': 5,
                'description': 'Refreshing smoothie packed with antioxidants and natural sweetness.',
                'pic': 'blueberry_smoothie.jpg'
            },
            {
                'name': 'Pad Thai',
                'ingredients': 'rice noodles, shrimp, tofu, eggs, peanuts, tamarind sauce',
                'cooking_time': 20,
                'description': 'Classic Thai stir-fried noodles with a perfect balance of sweet, sour, and savory flavors.',
                'pic': 'pad.thai.jpg'
            },
            {
                'name': 'Pesto Pasta',
                'ingredients': 'pasta, basil, pine nuts, parmesan cheese, olive oil, garlic',
                'cooking_time': 15,
                'description': 'Fresh basil pesto tossed with al dente pasta for a quick and delicious meal.',
                'pic': 'pesto.pasta.jpg'
            }
        ]

        created_count = 0
        for recipe_data in sample_recipes:
            # Check if recipe already exists
            if not Recipe.objects.filter(name=recipe_data['name']).exists():
                # Check if image file exists
                image_path = os.path.join('media', recipe_data['pic'])
                if os.path.exists(image_path):
                    recipe = Recipe.objects.create(
                        name=recipe_data['name'],
                        ingredients=recipe_data['ingredients'],
                        cooking_time=recipe_data['cooking_time'],
                        description=recipe_data['description'],
                        pic=recipe_data['pic']
                    )
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created recipe: {recipe.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Image file not found: {recipe_data["pic"]}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Recipe already exists: {recipe_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} recipes')
        ) 
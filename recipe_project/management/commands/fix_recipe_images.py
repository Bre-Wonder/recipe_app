from django.core.management.base import BaseCommand
from recipeApp.models import Recipe
import os

class Command(BaseCommand):
    help = 'Fix recipe image paths by matching recipe names to actual image files'

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        
        self.stdout.write(f"Found {recipes.count()} recipes in database")
        
        # Available image files
        media_dir = 'media'
        if os.path.exists(media_dir):
            image_files = os.listdir(media_dir)
            self.stdout.write(f"Available image files: {image_files}")
        else:
            self.stdout.write("Media directory not found!")
            return
        
        # Recipe name to image file mapping
        recipe_image_mapping = {
            'mochi': 'mochi.jpg',
            'iced vanilla latte': 'iced.vanilla.latte.jpg',
            'butter chicken': 'butter_chx.jpg',
            'spaghetti': 'spaghetti.jpg',
            'pad thai': 'pad.thai.jpg',
            'sourdough bread': 'sourdough.jpg',
            'lasagna': 'lasagna.jpg',
            'blueberry smoothie': 'blueberry_smoothie.jpg',
            'cobbler': 'cobbler.jpg',
            'mango sticky rice': 'mango_sticky_rice.jpg',
            'pesto pasta': 'pesto.pasta.jpg',
            'poke bowl': 'poke_bowl.jpg',
            'stroganoff': 'stroganoff.jpg',
            'broccoli cheddar soup': 'broccoli_cheddar_soup.jpg',
            'chicken noodle soup': 'chx_noodle_soup.jpg',
        }
        
        updated_count = 0
        for recipe in recipes:
            self.stdout.write(f"\nRecipe: {recipe.name}")
            self.stdout.write(f"Current pic field: {recipe.pic}")
            
            # Try to find matching image
            recipe_name_lower = recipe.name.lower()
            matching_image = None
            
            # First try exact mapping
            if recipe_name_lower in recipe_image_mapping:
                matching_image = recipe_image_mapping[recipe_name_lower]
                self.stdout.write(f"Found exact match: {matching_image}")
            
            # If no exact match, try partial matching
            if not matching_image:
                for image_file in image_files:
                    if image_file.endswith('.jpg') or image_file.endswith('.png'):
                        # Remove extension and replace dots/underscores with spaces
                        image_name = image_file.replace('.jpg', '').replace('.png', '').replace('.', ' ').replace('_', ' ')
                        if recipe_name_lower in image_name.lower() or image_name.lower() in recipe_name_lower:
                            matching_image = image_file
                            self.stdout.write(f"Found partial match: {matching_image}")
                            break
            
            # Update recipe if we found a matching image
            if matching_image:
                if str(recipe.pic) != matching_image:
                    recipe.pic = matching_image
                    recipe.save()
                    self.stdout.write(f"Updated recipe '{recipe.name}' with image: {matching_image}")
                    updated_count += 1
                else:
                    self.stdout.write(f"Recipe '{recipe.name}' already has correct image: {matching_image}")
            else:
                # Set default image if no match found
                if not recipe.pic or str(recipe.pic) == 'no_picture.jpg':
                    recipe.pic = 'no_picture.jpg'
                    recipe.save()
                    self.stdout.write(f"Set default image for recipe '{recipe.name}'")
                else:
                    self.stdout.write(f"No matching image found for recipe '{recipe.name}'")
        
        self.stdout.write(f"\nUpdated {updated_count} recipes with correct images!")
        self.stdout.write("Recipe image fix completed!") 
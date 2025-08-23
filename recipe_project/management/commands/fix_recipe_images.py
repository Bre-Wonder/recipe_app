from django.core.management.base import BaseCommand
from recipeApp.models import Recipe
import os

class Command(BaseCommand):
    help = 'Check and fix recipe image paths'

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        
        self.stdout.write(f"Found {recipes.count()} recipes in database")
        
        for recipe in recipes:
            self.stdout.write(f"\nRecipe: {recipe.name}")
            self.stdout.write(f"Current pic field: {recipe.pic}")
            self.stdout.write(f"Current pic name: {recipe.pic.name if recipe.pic else 'None'}")
            self.stdout.write(f"Current pic URL: {recipe.pic.url if recipe.pic else 'None'}")
            
            # Check if the image file exists
            if recipe.pic:
                image_path = os.path.join('media', str(recipe.pic))
                file_exists = os.path.exists(image_path)
                self.stdout.write(f"Image file exists: {file_exists}")
                
                # Try to find the correct image file
                if not file_exists:
                    # Look for similar files in media directory
                    media_dir = 'media'
                    if os.path.exists(media_dir):
                        files = os.listdir(media_dir)
                        matching_files = [f for f in files if recipe.name.lower().replace(' ', '') in f.lower().replace(' ', '').replace('.', '')]
                        
                        if matching_files:
                            self.stdout.write(f"Found matching files: {matching_files}")
                            # Update the recipe with the correct image
                            recipe.pic = matching_files[0]
                            recipe.save()
                            self.stdout.write(f"Updated recipe {recipe.name} with image: {matching_files[0]}")
                        else:
                            self.stdout.write("No matching image files found")
            else:
                self.stdout.write("No image assigned to this recipe")
                
        self.stdout.write("\nRecipe image check completed!") 
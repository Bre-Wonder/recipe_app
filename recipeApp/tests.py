from django.test import TestCase, Client
from .models import Recipe
from django.urls import reverse
# to access Recipe model
from django.db import models
from recipeApp.forms import IngredientSearchForm, ChartForm
from django.contrib.auth.models import User


# Create your tests here.


class RecipeModelTest(TestCase):

    def setUpTestData():
        Recipe.objects.create(name='Spaghetti', ingredients='Meatballs, Noodles, Tomato Sauce',
                              cooking_time=25, difficulty='medium', description='Gather around with your family for warm fall meal. The tomatoes are flavorful and the noodles hit the spot. Join in and enjoy this recipe.')

    def test_recipe_name(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'name' field and use it to query its data
        field_label = recipe._meta.get_field('name').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'name')

    def test_ingredients_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'ingredients' field and use it to query its max_length
        max_length = recipe._meta.get_field('ingredients').max_length

        # Compare the value to the expected result i.e. 255
        self.assertEqual(max_length, 255)

    def test_cooking_time_type(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'cooking_time' field and use it to query if its an integer
        field = recipe._meta.get_field('cooking_time')

        # checkes if cooking_time is an integer
        self.assertIsInstance(field, models.IntegerField)

    def test_difficulty_type(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'difficulty' field
        field = recipe._meta.get_field('difficulty')

        # Check if 'difficulty' is a CharField (string)
        self.assertIsInstance(field, models.CharField)

    def test_recipe_description(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'description' field and use it to query its data
        field_label = recipe._meta.get_field('description').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'description')

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        # get_absolute_url() should take you to the detail page of recipe #1
        self.assertEqual(recipe.get_absolute_url(), '/list/1')


class RecipeFormTest(TestCase):

    # testing that search bar accepts valid data
    def test_search_accepts_valid_data(self):
        form = IngredientSearchForm(data={'recipe_title': 'Pizza'})
        self.assertTrue(form.is_valid())

    # ensuring that user input doesn't exceed character length
    def test_form_max_length(self):
        long_title = 'x' * 121
        form = IngredientSearchForm(data={'recipe_title': long_title})
        self.assertFalse(form.is_valid())

    # testing that chart form accepts valid choice from options
    def test_chart_accepts_valid_data(self):
        form = ChartForm(data={'chart_type': '#1'})
        self.assertTrue(form.is_valid())

    # ensures required fied is not optional
    def test_chart_form_requires_chart_type(self):
        form = ChartForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('chart_type', form.errors)


class RecipeViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser', password='testpass')
        cls.recipe = Recipe.objects.create(
            name='Pasta',
            cooking_time=20,
            ingredients='noodles, sauce',
            difficulty='Easy',
            description='Test description'
        )

    def setUp(self):
        self.client = Client()

    # checks that home page is accessible without login and use the correct template
    def test_home_view(self):
        response = self.client.get(reverse('recipeApp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipeApp/recipe_home.html')

    # confirms that login is required for access
    def test_recipe_list_view_requires_login(self):
        response = self.client.get(reverse('recipeApp:list'))
        self.assertRedirects(response, '/login/?next=' +
                             reverse('recipeApp:list'))

    # confirms that list view page loads once user is authenticated
    def test_recipe_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('recipeApp:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipeApp/main_recipelist.html')
        self.assertIn('form', response.context)

    # confirms that login is required for access

    def test_recipe_detail_view_requires_login(self):
        response = self.client.get(
            reverse('recipeApp:detail', args=[self.recipe.id]))
        self.assertRedirects(response, f'/login/?next=/list/{self.recipe.id}')

    # confirms that detail view renders once user is authenticated
    def test_recipe_detail_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(
            reverse('recipeApp:detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipeApp/recipe_details.html')
        self.assertEqual(response.context['object'], self.recipe)

    # tests if the difficulty chart view processes form and chart logic

    def test_difficulty_chart_view_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipeApp:charts'), {
            'chart_type': '#1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipeApp/charts.html')
        self.assertIn('chart', response.context)

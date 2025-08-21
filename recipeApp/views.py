from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe
# authentication required with for classes
from django.contrib.auth.mixins import LoginRequiredMixin
# authentication required for functions
from django.contrib.auth.decorators import login_required
# import form from forms.py
from .forms import IngredientSearchForm, ChartForm, CreateRecipe
# installed pandas, now importing it
import pandas as pd
# allows queries to use the OR operator
from django.db.models import Q
from .utils import get_chart
# import for success messages once user completes a form
from django.contrib import messages


# Create your views here.


class RecipeListView(LoginRequiredMixin, ListView):
    # model that is being communicated with
    model = Recipe
    # template that is being used
    template_name = 'recipeApp/main_recipelist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IngredientSearchForm()
        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
  # model that is being communicated with
    model = Recipe
    # template that is being used
    template_name = 'recipeApp/recipe_details.html'


def home(request):
    return render(request, 'recipeApp/recipe_home.html')


def about(request):
    return render(request, 'recipeApp/about.html')

 # function that send in form for the user


@login_required
def IngredientSearch(request):
  # creates an instance of the form
    form = IngredientSearchForm(request.POST or None)
    recipeApp_df = None

    # checks to see if search button is clicked
    if request.method == 'POST':
        # reads recipe_title
        recipe_title = request.POST.get('recipe_title')
        print(recipe_title)

        # filter for user to be able to find recipe name and ingredients in the Recipe object
        qs = Recipe.objects.filter(Q(name__icontains=recipe_title) | Q(
            ingredients__icontains=recipe_title))
        print(qs)

    # packs up dtat to be sent to template in the form of a dictionary
    context = {
        'form': form,
        'qs': qs
    }

    return render(request, 'recipeApp/ingredient_search.html', context)


@login_required
def DifficultyChart(request):
    # creates an instance of a form
    form = ChartForm(request.POST or None)
    # initialized DataFrame as None
    recipeApp_df = None
    chart = None

    if request.method == 'POST':
        # reads chart_type
        chart_type = request.POST.get('chart_type')
        print(chart_type)

        # Get ALL recipes (not filtered by chart_type)
        qs = Recipe.objects.all()

        if qs.exists():
            # Create DataFrame from all recipes
            recipeApp_df = pd.DataFrame(qs.values())

            # Count recipes by difficulty level
            difficulty_counts = recipeApp_df['difficulty'].value_counts()

            # Create a new DataFrame for charting with the correct structure
            chart_df = pd.DataFrame({
                'difficulty': difficulty_counts.index,
                'quantity': difficulty_counts.values
            })

            chart = get_chart(chart_type, chart_df,
                              labels=chart_df['difficulty'].values)

    context = {
        'form': form,
        'recipeApp_df': recipeApp_df,
        'chart': chart
    }
    return render(request, 'recipeApp/charts.html', context)

# allows user to created their own recipe


@login_required
def create_recipe(request):
    if request.method == 'POST':
        # creates instance of a form
        form = CreateRecipe(request.POST, request.FILES)
        if form.is_valid():
            # saves the inputs of this form
            form.save()
            # sends message to the user that recipe was added successfully
            messages.success(request, 'Recipe was added successfully')
            return redirect('recipeApp:list')
    else:
        form = CreateRecipe()

    context = {
        'form': form
    }

    return render(request, 'recipeApp/create_recipe.html', context)

from django import forms
from .models import Recipe

# chart options
CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart')
)

# class created for form to be used


class IngredientSearchForm(forms.Form):
    # defined form type
    recipe_title = forms.CharField(max_length=120, label="Recipe Lookup")

# class created for chart form to be used


class ChartForm(forms.Form):
    # create chart form and added choices
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)

# created user input form for user to be able to add recipe


class CreateRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'description', 'pic']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 5},)
        }

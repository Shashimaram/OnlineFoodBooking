from django import forms
from .models import Category, Fooditem
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name', 'description']

class FooditemForm(forms.ModelForm):


    class Meta:
        model = Fooditem
        fields = ['food_title', 'description','price', 'image','is_available','category']

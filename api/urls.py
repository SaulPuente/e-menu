from pathlib import Path
from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.default,name="default"),
    # this is the home url
    path('home', views.home, name='home'),
    # this is the single book url
    path('recipe-detail/<str:id>/', views.recipe_detail, name='recipe-detail'),
    # this is the add book url
    path('add-recipe/', views.add_recipe, name='add-recipe'),
    # this is the edit book url
    path('edit-recipe/<str:id>/', views.edit_recipe, name='edit-recipe'),
    # this is the delete book url
    path('delete-recipe/<str:id>/', views.delete_recipe, name='delete-recipe'),
    path("test/", views.test.as_view()),
    path("register/", views.register.as_view()),
    path("login/", views.login.as_view()),
    path("newRecipe/", views.newRecipe.as_view()),
    path("recipe/", views.recipe.as_view()),
    path("recipes/", views.recipes.as_view()),
    path("updateRecipe/", views.updateRecipe.as_view()),
    path("deleteRecipe/", views.deleteRecipe.as_view()),
]

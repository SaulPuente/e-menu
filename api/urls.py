from pathlib import Path
from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.default,name="default"),
    path("test/", views.test.as_view()),
    path("register/", views.register.as_view()),
    path("login/", views.login.as_view()),
    path("newRecipe/", views.newRecipe.as_view()),
    path("recipe/", views.recipe.as_view()),
    path("recipes/", views.recipes.as_view()),
    path("updateRecipe/", views.updateRecipe.as_view()),
    path("deleteRecipe/", views.deleteRecipe.as_view()),
]

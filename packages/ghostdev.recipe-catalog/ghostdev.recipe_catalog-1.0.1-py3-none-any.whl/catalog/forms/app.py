from collections import OrderedDict

import wx
from pyform import Form, FormDialog
from pyform.Controls import Button

from .ingredients import AddIngredient, ListIngredients
from .recipes import ListRecipes, Recipe, SearchRecipes


class App(Form):
    def __init__(self, parent, **kwargs):
        self.form = form = dict(
            Title="Recipe Catalog",
        )
        parts = form["Parts"] = OrderedDict()
        parts["Ingredients"] = ingredients = list()
        ingredients.append(
            (
                Button(name="add_ingredient", label="Add"),
                Button(name="list_ingredients", label="List"),
            )
        )
        parts["Recipes"] = recipes = list()
        recipes.append(
            (
                Button(name="add_recipe", label="Add"),
                Button(name="list_recipes", label="List"),
                Button(name="search_recipes", label="Search"),
            )
        )
        super(App, self).__init__(parent, **kwargs)

    def bind(self):
        self.Bind(wx.EVT_BUTTON, self.on_add_ingredient, "add_ingredient")
        self.Bind(wx.EVT_BUTTON, self.on_list_ingredients, "list_ingredients")
        self.Bind(wx.EVT_BUTTON, self.on_add_recipe, "add_recipe")
        self.Bind(wx.EVT_BUTTON, self.on_list_recipes, "list_recipes")
        self.Bind(wx.EVT_BUTTON, self.on_search_recipes, "search_recipes")

    def on_search_recipes(self, evt=None):
        FormDialog(self, SearchRecipes)

    def on_list_recipes(self, evt=None):
        FormDialog(self, ListRecipes)

    def on_add_ingredient(self, evt=None):
        FormDialog(self, AddIngredient)

    def on_list_ingredients(self, evt=None):
        FormDialog(self, ListIngredients)

    def on_add_recipe(self, evt=None):
        FormDialog(self, Recipe)

from collections import OrderedDict

import wx
from pyform import Form, FormDialog
from pyform.Controls import CheckBox, CheckListBox, ListBox, TextCtrl

from catalog.storage.sqlite import Sqlite

PARTS = "Parts"


class Recipe(Form):
    def __init__(self, parent, recipe=None, **kwargs):
        self.form = dict(
            Title="Add Recipe",
            Defaults={"ingredients": []},
        )
        if recipe is not None:
            self.form["Defaults"] = defaults = {"ingredients": []}
            cols, *rows = Sqlite.get_recipe_by_name(recipe)
            for row in rows:
                for col, field in zip(cols, row):
                    if col == "ingredients":
                        defaults["ingredients"].append(field)
                    else:
                        defaults[col] = field
        self.form[PARTS] = parts = OrderedDict()
        parts["Recipe Name"] = [
            TextCtrl(name="recipe_name", size=(300, -1)),
        ]
        parts["External Location"] = [
            TextCtrl(name="external_location"),
        ]
        parts["Ingredients"] = [
            CheckListBox(
                name="ingredients", choices=Sqlite.list_ingredients, size=(-1, 100)
            ),
        ]
        parts["Notes", Form.G] = [
            TextCtrl(name="notes", style=wx.TE_MULTILINE, proportion=1, size=(300, 200))
        ]
        super().__init__(parent, **kwargs)

    def onOk(self, evt):
        Sqlite.add_recipe(**dict(self))
        super().onOk(evt)


class HasRecipeList:
    def on_recipe_activate(self, evt=None):
        FormDialog(self, Recipe, recipe=evt.String)


class ListRecipes(HasRecipeList, Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(
            Title="Known Recipes",
        )
        self.form[PARTS] = parts = OrderedDict()
        parts["", Form.NC] = [ListBox(name="recipes", choices=Sqlite.list_recipes)]
        super().__init__(parent, **kwargs)

    def bind(self):
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_recipe_activate, "recipes")


class SearchRecipes(HasRecipeList, Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(
            Title="Search Recipes",
        )
        self.form[PARTS] = parts = OrderedDict()
        parts["Ingredients", Form.G] = [
            CheckListBox(
                name="ingredients",
                choices=Sqlite.list_ingredients,
                size=(-1, 100),
                proportion=1,
            ),
        ]
        parts["", Form.NC] = [
            CheckBox(name="reverse", label="Reverse search (exclude ingredients)")
        ]
        parts["Recipe Options", Form.G] = [
            ListBox(name="recipes", choices=Sqlite.list_recipes, proportion=1)
        ]
        super().__init__(parent, **kwargs)

    def bind(self):
        self.Bind(wx.EVT_CHECKLISTBOX, self.on_ingredient_checked, "ingredients")
        self.Bind(wx.EVT_CHECKBOX, self.on_ingredient_checked, "reverse", True)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_recipe_activate, "recipes")

    def on_ingredient_checked(self, evt=None):
        if self["reverse"]:
            recipes = Sqlite.search_recipes_without(self["ingredients"])
        else:
            recipes = Sqlite.search_recipes_with(self["ingredients"])
        self.elements["recipes"].SetItems(recipes)

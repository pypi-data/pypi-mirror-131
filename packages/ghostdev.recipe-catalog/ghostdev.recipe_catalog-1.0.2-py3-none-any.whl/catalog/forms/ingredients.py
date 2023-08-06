from collections import OrderedDict

import wx
from pyform import Form
from pyform.Controls import ListBox, TextCtrl

from catalog.storage.sqlite import Sqlite

PARTS = "Parts"


class AddIngredient(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(
            Title="Add Ingredient",
        )
        self.form[PARTS] = parts = OrderedDict()
        parts["Ingredient Name", Form.G] = [
            TextCtrl(name="name", size=(200, -1)),
        ]
        super().__init__(parent, **kwargs)

    def onOk(self, evt):
        Sqlite.add_ingredient(self.elements["name"].GetValue())
        super().onOk(evt)


class ListIngredients(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(
            Title="Known Ingredients",
            AddButtons=dict(
                Delete=wx.NewIdRef(1),
                Ok=wx.ID_OK,
            ),
        )
        self.form[PARTS] = parts = OrderedDict()
        parts["", Form.NC] = [
            ListBox(
                name="ingredients", choices=Sqlite.list_ingredients, size=(300, 200)
            ),
        ]
        super().__init__(parent, **kwargs)

    def onDelete(self, evt=None):
        ingredient = self["ingredients"]
        element = self.elements["ingredients"]
        dlg = wx.MessageDialog(self, f"Are you sure you want to delete '{ingredient}'?", "Confirm", style=wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            Sqlite.delete_ingredient(ingredient)
            element.Delete(element.GetSelection())


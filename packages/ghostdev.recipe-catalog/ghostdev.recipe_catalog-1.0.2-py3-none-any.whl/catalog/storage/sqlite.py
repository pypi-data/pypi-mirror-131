import atexit
import sqlite3
from os import path

INGREDIENTS = "Ingredients"
RECIPES = "Recipes"


class Sqlite:
    def __init__(self):
        self.db = sqlite3.connect("catalog.db")
        self.init_schema()
        atexit.register(self.db.close)

    def init_schema(self):
        with open(path.join(path.dirname(__file__), "sqlite.schema")) as schema:
            self.db.executescript(schema.read())

    def add_ingredient(self, ingredient):
        self.dml("INSERT INTO ingredient (ingredient_name) VALUES (?)", [ingredient])

    @property
    def list_ingredients(self):
        # The query method includes column names as the first record, return just the
        # ingredients themselves here.
        return [
            row[0]
            for row in self.query(
                "SELECT ingredient_name FROM ingredient ORDER BY ingredient_name"
            )[1:]
        ]

    def add_recipe(self, recipe_name, external_location, notes, ingredients):
        self.dml(
            "INSERT INTO "
            "  recipe (recipe_name, external_location, notes) "
            "VALUES "
            "  (?, ?, ?) "
            "ON CONFLICT DO UPDATE SET "
            "  notes = excluded.notes",
            [recipe_name, external_location, notes],
        )
        recipe_id = self.get_recipe_id(recipe_name)
        self.sync_recipe_ingredients(recipe_id, ingredients)

    def sync_recipe_ingredients(self, recipe_id, ingredients):
        qmarks = ','.join('?' for _ in ingredients)
        query = f"SELECT ingredient_id FROM ingredient WHERE ingredient_name IN ({qmarks})"
        result = self.query(query, ingredients)
        ingredient_ids = [r for (r,) in result[1:]]
        query = f"DELETE FROM recipe_ingredients WHERE recipe_id = ? AND ingredient_id NOT IN ({qmarks})"
        self.dml(query, [recipe_id] + ingredient_ids)
        self.dmls(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id) "
            "VALUES (?, ?) "
            "ON CONFLICT DO NOTHING",
            [[recipe_id, ingredient_id] for ingredient_id in ingredient_ids],
        )

    def get_recipe_id(self, recipe_name):
        return self.query("SELECT recipe_id FROM recipe WHERE recipe_name = ?", [recipe_name])[1][0]

    @property
    def list_recipes(self):
        # The query method includes column names as the first record, return just the
        # recipes themselves here.
        return [
            row[0]
            for row in self.query(
                "SELECT recipe_name FROM recipe ORDER BY recipe_name"
            )[1:]
        ]

    def get_recipe_by_name(self, recipe):
        query = (
            "SELECT recipe_name, external_location, notes, ingredient_name as ingredients "
            "FROM recipe r "
            "INNER JOIN "
            "  recipe_ingredients ri on r.recipe_id = ri.recipe_id "
            "INNER JOIN "
            "  ingredient i on i.ingredient_id = ri.ingredient_id "
            "WHERE recipe_name = ?"
        )
        return self.query(query, [recipe])

    def search_recipes_with(self, ingredients):
        query = (
            "SELECT DISTINCT "
            "  recipe_name "
            "FROM "
            "  recipe "
            "INNER JOIN "
            "  recipe_ingredients ri on recipe.recipe_id = ri.recipe_id "
            "INNER JOIN "
            "  ingredient i on ri.ingredient_id = i.ingredient_id "
            "WHERE "
            f"  ingredient_name IN ({', '.join(['?'] * len(ingredients))}) "
            "ORDER BY "
            "  recipe_name"
        )
        return [row[0] for row in self.query(query, ingredients)[1:]]

    def search_recipes_without(self, ingredients):
        query = (
            "SELECT "
            "  recipe_name "
            "FROM "
            "  recipe r "
            "EXCEPT SELECT "
            "  recipe_name "
            "FROM "
            "  recipe r2 "
            "INNER JOIN "
            "  recipe_ingredients ri2 on r2.recipe_id = ri2.recipe_id "
            "INNER JOIN "
            "  ingredient i on ri2.ingredient_id = i.ingredient_id "
            "WHERE "
            f"  i.ingredient_name in ({(','.join(['?'] * len(ingredients)))}) "
            "ORDER BY "
            "  recipe_name"
        )
        return [row[0] for row in self.query(query, ingredients)[1:]]

    def delete_ingredient(self, ingredient):
        self.dml("DELETE FROM ingredient WHERE ingredient_name = ?", [ingredient])

    def query(self, query, params=None):
        cursor = self.db.cursor()
        self.execute(cursor, query, params)
        return [[x[0] for x in cursor.description]] + list(cursor.fetchall())

    def dml(self, query, params=None):
        cursor = self.db.cursor()
        self.execute(cursor, query, params)
        self.db.commit()

    def dmls(self, query, params=None):
        cursor = self.db.cursor()
        self.execute_many(cursor, query, params)
        self.db.commit()

    @staticmethod
    def execute(cursor: sqlite3.Cursor, query, params=None):
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        except Exception as e:
            print(e)

    @staticmethod
    def execute_many(cursor: sqlite3.Cursor, query, params):
        try:
            cursor.executemany(query, params)
        except Exception as e:
            print(e)


Sqlite = Sqlite()

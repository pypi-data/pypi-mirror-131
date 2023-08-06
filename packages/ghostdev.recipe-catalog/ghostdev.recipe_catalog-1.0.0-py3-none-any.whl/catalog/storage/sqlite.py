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
            "INSERT INTO recipe (recipe_name, external_location, notes) VALUES (?, ?, ?)",
            [recipe_name, external_location, notes],
        )
        recipe_id = self.last_id
        self.dmls(
            "INSERT INTO recipe_ingredients (ingredient_id, recipe_id) "
            "VALUES ((SELECT ingredient_id FROM ingredient WHERE ingredient_name = ?), ?)",
            [[ingredient, recipe_id] for ingredient in ingredients],
        )

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

    @property
    def last_id(self):
        return self.db.execute("SELECT last_insert_rowid()").fetchall()[0][0]

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

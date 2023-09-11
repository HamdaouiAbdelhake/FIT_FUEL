import json

from flask import redirect, render_template, session
from functools import wraps
from urllib.request import urlopen
from datetime import datetime


KEY = "DVfczk7JSbdPtyOEriIcDRxr6CQOS8PAKaz3Df5Q"
CATEGORIES = ["American Indian/Alaska Native Foods","Baby Foods","Baked Products","Beef Products","Beverages","","Breakfast Cereals","Cereal Grains and Pasta","Fast Foods","Fats and Oils","Finfish and Shellfish Products","Fruits and Fruit Juices","Lamb, Veal, and Game Products","Legumes and Legume Products","Meals, Entrees, and Side Dishes","Nut and Seed Products","Pork Products","Poultry Products","Restaurant Foods","Sausages and Luncheon Meats","Snacks","Soups, Sausages, and Gravies","Spices and Herbs","Sweets","Vegetables and Vegetable Products"]
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(query , category_index):
    query = query.replace(" " , "%20")
    category = CATEGORIES[category_index - 1]
    category = category.replace(" " , "%20")
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={KEY}&query={query}&dataType=SR%20Legacy&requireAllWords=true&foodCategory={category}"
    response = urlopen(url)

    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())
    if data_json["totalHits"] == 0:
        return False
    result = []
    # print the json response
    for i in data_json["foods"]:
        element = {"name" : i["description"],"id" : i["fdcId"]}
        for j in i["foodNutrients"]:
            if j["nutrientName"] in ["Energy","Protein","Total lipid (fat)","Carbohydrate, by difference"]:
                element[j["nutrientName"]] = j["value"]
        result.append(element)
    return result

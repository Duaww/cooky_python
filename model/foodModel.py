from pymongo import MongoClient
from pymongo import collection
import pymongo
from schematics.models import Model
import schematics.types
from schematics.types.base import StringType
import json
from fastapi import FastAPI

url = "mongodb+srv://lvl162:1622000@cluster0.gabg8.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = MongoClient(url)
database = client['CookyCooky']
foodCollection = database.get_collection("recipes") 
from fastapi import APIRouter



def foodSchema(food) -> dict:
    return {
        "cooking_steps" : food['cooking_steps'],
        "name" : food['name'],
        "description" : food['description'],
        "ingredients" : food['ingredients'],
        "image" : food['image'],
        "ration" : food['ration'],
        "likes" : food['likes'],
        "id" : food['id']
    }



async  def foodGetAll():
    foods = []
    for  food in foodCollection.find():
        foods.append(foodSchema(food))
    return foods

async def foodGetId(id : int):
    food = foodCollection.find_one({"id" : id})
    return foodSchema(food)


def sortByLikes(food):
    return -food['likes']

async def foodSearchByName(name : str):
    foods = await foodGetAll()
    matchFood = []
    name = name.lower()
    for food in foods:
        foodName = food['name'].lower()
        if(foodName.find(name) >= 0):
            matchFood.append(food)
    matchFood.sort(key=sortByLikes)
    return matchFood





app = FastAPI()

@app.get("/food/{id}")
async def getId(id):
    food = await foodGetId(int(id))
    return {"food" : food}

@app.get("/food")
async def getAll():
    foods = await foodGetAll()
    return {"food" : foods}

@app.get("/food/search/{name}")
async def searchByName(name):
    matchFood = await foodSearchByName(name)
    return {"matchFood" : matchFood }
    

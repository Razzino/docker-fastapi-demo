from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class RecipeBase(BaseModel):
    name: str
    ingredients: str
    steps: str
    prep_time: int

class RatingBase(BaseModel):
    rating: int

class CommentBase(BaseModel):
    text: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Create a new recipe
@app.post("/recipes/", status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeBase, db: db_dependency):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe



# Retrieve a list of all recipes, sorted by most recent
@app.get("/recipes/", status_code=status.HTTP_200_OK)
async def read_recipes(db: db_dependency):
    recipes = db.query(models.Recipe).order_by(models.Recipe.created_at.desc()).all()
    return recipes



# Retrieve details of a specific recipe by its ID
@app.get("/recipes/{recipe_id}", status_code=status.HTTP_200_OK)
async def read_recipe(recipe_id: int, db: db_dependency):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe



# Update a specific recipe by its ID
@app.put("/recipes/{recipe_id}", status_code=status.HTTP_200_OK)
async def update_recipe(recipe_id: int, recipe: RecipeBase, db: db_dependency):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db_recipe.name = recipe.name
    db_recipe.ingredients = recipe.ingredients
    db_recipe.steps = recipe.steps
    db_recipe.prep_time = recipe.prep_time
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe



# Delete a specific recipe by its ID
@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_200_OK)
async def delete_recipe(recipe_id: int, db: db_dependency):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return {"detail": "Recipe deleted"}



# Rate a specific recipe
@app.post("/recipes/{recipe_id}/ratings/", status_code=status.HTTP_201_CREATED)
async def rate_recipe(recipe_id: int, rating: RatingBase, db: db_dependency):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_rating = models.Rating(rating=rating.rating, recipe_id=recipe_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating



# Comment on a specific recipe
@app.post("/recipes/{recipe_id}/comments/", status_code=status.HTTP_201_CREATED)
async def comment_recipe(recipe_id: int, comment: CommentBase, db: db_dependency):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_comment = models.Comment(text=comment.text, recipe_id=recipe_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment



# Retrieve all comments for a specific recipe
@app.get("/recipes/{recipe_id}/comments/", status_code=status.HTTP_200_OK)
async def get_comments(recipe_id: int, db: db_dependency):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    comments = db.query(models.Comment).filter(models.Comment.recipe_id == recipe_id).all()
    return comments

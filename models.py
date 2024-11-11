from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    ingredients = Column(String(500))
    steps = Column(String(1000))
    prep_time = Column(Integer)  # in minutes
    created_at = Column(Integer)  # Timestamp

    ratings = relationship("Rating", back_populates="recipe")
    comments = relationship("Comment", back_populates="recipe")

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)  # Rating from 1 to 5
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

    recipe = relationship("Recipe", back_populates="ratings")

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

    recipe = relationship("Recipe", back_populates="comments")

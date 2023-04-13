import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from ..constants.environmet import APIS, ENDPOINTS, JOKES
from ..schemas import jokes
from . import models


def get_external_api(api_key: str) -> dict[str, str]:
    """
    Get a random joke from an external API.

    Args:
        api_key (str): The key for the API.

    Returns:
        dict[str, str]: A dictionary containing the joke.
    """
    api = APIS[api_key]
    endpoint = ENDPOINTS[api_key]["random"]
    joke = JOKES[api_key]

    url = api + endpoint
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers).json()[joke]
    return {"joke": response}


def get_random_joke(db: Session) -> jokes.Joke:
    """
    Get a random joke from the database.

    Args:
        db (Session): The database session.

    Returns:
        jokes.Joke: The joke object.

    Raises:
        HTTPException: If no joke is found.
    """
    random_joke = db.query(models.JokeTable).order_by(func.random()).first()
    if not random_joke:
        raise HTTPException(status_code=404, detail="You have no jokes")
    return random_joke


def existing_joke(joke: str, db: Session) -> None:
    """
    Check if a joke already exists in the database.

    Args:
        joke (str): The joke to check.
        db (Session): The database session.

    Raises:
        HTTPException: If the joke already exists in the database.
    """
    db_joke = db.query(
        models.JokeTable).filter(
        models.JokeTable.joke == joke).first()
    if db_joke:
        raise HTTPException(status_code=400, detail="Joke already exists")


def get_joke(joke_id: int, db: Session) -> jokes.Joke:
    """
    Get a joke from the database by its ID.

    Args:
        joke_id (int): The ID of the joke to get.
        db (Session): The database session.

    Returns:
        jokes.Joke: The joke object.

    Raises:
        HTTPException: If the joke is not found.
    """
    db_joke = db.get(models.JokeTable, joke_id)
    if db_joke:
        return db_joke
    else:
        raise HTTPException(status_code=404, detail="Joke not found")


def get_joke_by_id(joke_id: int, db: Session) -> jokes.Joke:
    """
    Get a joke from the database by its ID.

    Args:
        joke_id (int): The ID of the joke to get.
        db (Session): The database session.

    Returns:
        jokes.Joke: The joke object.
    """
    return db.query(
        models.JokeTable).filter(
        models.JokeTable.id == joke_id).first()


def create_joke(joke: jokes.JokeCreate, db: Session) -> jokes.Joke:
    """
    Create a new joke in the database.

    Args:
        joke (jokes.JokeCreate): The joke to create.
        db (Session): The database session.

    Returns:
        jokes.Joke: The created joke object.
    """
    db_joke = models.JokeTable(joke=joke.joke)
    db.add(db_joke)
    db.commit()
    db.refresh(db_joke)
    return db_joke


def delete_joke(joke_id: int, db: Session) -> dict[str, str]:
    """
    Delete a joke from the database by its ID.

    Args:
        joke_id (int): The ID of the joke to delete.
        db (Session): The database session.

    Returns:
        dict[str, str]: A dictionary containing a message confirming the
            deletion.

    Raises:
        HTTPException: If the joke is not found.
    """
    db_joke = get_joke(joke_id, db)
    db.delete(db_joke)
    db.commit()
    return {"message": f"Joke n°{db_joke.id} removed: {db_joke.joke}"}

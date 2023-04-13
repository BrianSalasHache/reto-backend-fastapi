from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import crud
from ..db.db import get_db
from ..schemas import jokes

router = APIRouter(prefix="/jokes", tags=["jokes"])


@router.get("/")
def get_joke(api: str | None = None, db: Session = Depends(get_db)):
    """
    Get a joke.

    Args:

        api (str | None): The external API to use to retrieve a joke. Only
            accepts "Chuck" or "Dad".
        db (Session, optional): The database session. Defaults to
            Depends(get_db).

    Returns:

        Joke: A joke object retrieved from the specified API, or a random joke
            from the database.

    Raises:

        HTTPException: Raised if an invalid API is specified.
    """
    if not api:
        return crud.get_random_joke(db)

    match api:
        case "Chuck":
            return crud.get_external_api("Chuck")
        case "Dad":
            return crud.get_external_api("Dad")
        case _:
            raise HTTPException(
                status_code=400, detail="You can only enter 'Chuck' or 'Dad'")


@router.post("/", response_model=jokes.Joke, status_code=201)
def create_joke(
        joke: jokes.JokeCreate,
        db: Session = Depends(get_db)) -> jokes.Joke:
    """
    Create a new joke.

    Args:

        joke (JokeCreate): A joke creation object.
        db (Session, optional): The database session. Defaults to
            Depends(get_db).

    Returns:

        Joke: The newly created joke.

    Raises:

        HTTPException: Raised if the joke already exists.
    """
    crud.existing_joke(joke.joke, db)

    return crud.create_joke(joke, db)


@router.put("/{joke_id}", response_model=jokes.Joke)
def update_joke(joke_id: int,
                joke_update: jokes.JokeUpdate,
                db: Session = Depends(get_db)) -> jokes.Joke:
    """
    Update an existing joke.

    Args:

        joke_id (int): The ID of the joke to update.
        joke_update (JokeUpdate): A joke update object.
        db (Session, optional): The database session. Defaults to
            Depends(get_db).

    Returns:

        Joke: The updated joke.

    Raises:

        HTTPException: Raised if the joke to update already exists or if the
            joke_id does not exist.
    """
    db_joke = crud.get_joke(joke_id, db)
    crud.existing_joke(joke_update.joke, db)

    db_joke.joke = joke_update.joke
    db.commit()

    return db_joke


@router.delete("/{joke_id}")
def delete_joke_by_id(
        joke_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Delete a joke.

    Args:

        joke_id (int): The ID of the joke to delete.
        db (Session, optional): The database session. Defaults to
            Depends(get_db).

    Returns:

        Dict[str, str]: A dictionary with a message confirming that the joke
            was deleted.

    Raises:

        HTTPException: Raised if the joke_id to delete does not exist.
    """
    return crud.delete_joke(joke_id, db)

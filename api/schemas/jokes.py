from fastapi import HTTPException
from pydantic import BaseModel, validator


class JokeBase(BaseModel):
    joke: str

    @validator('joke')
    def joke_min_length(cls, v: str) -> str:
        """
        Validates the length of the joke string.

        Args:
            v (str): The joke string.

        Raises:
            HTTPException: if the joke is less than 5 characters long.

        Returns:
            v (str): The joke.
        """
        min_chars = 5
        if len(v) < min_chars:
            raise HTTPException(
                status_code=400,
                detail=f"Joke must be at least {min_chars} characters long")
        return v


class JokeCreate(JokeBase):
    pass


class JokeRead(JokeBase):
    pass


class JokeUpdate(JokeBase):
    pass


class JokeDelete(JokeBase):
    id: int


class Joke(JokeBase):
    id: int

    class Config:
        orm_mode = True

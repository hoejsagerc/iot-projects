
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    device: str
    temp: Union[float, None]


app = FastAPI()


@app.post("/temps/")
async def create_item(item: Item):
    print(item)
    return item

## Python
from enum import Enum
from typing import Optional, List, Dict
## Pydantic
from pydantic import BaseModel
from pydantic import Field

## FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

## Local Modules

app = FastAPI()


class StatusContainerEnum(Enum):
    empty= 'empty',
    filling = 'filling'
    ready= 'ready'
    filled= 'filled'

## Models
class Container(BaseModel):
    volume: float = Field(
        ...,
        ge=0,
        title='Volume',
        description='This value describes the capacity of the garbage container',
        example=4000.25
    )
    status: StatusContainerEnum = StatusContainerEnum.ready
    latitude: float = Field(
        ...,
        title='Latitude',
        description='Latitude where a container is located',
        example=11.53952
    )
    longitude: float = Field(
        ...,
        title='Longitude',
        description='Longitude where a container is located',
        example=-72.92859
    )

class Route(BaseModel):
    route_list: List[Dict[str, float]] = Field(
        example = [
            {'lat': 11.54752, 'lon': -72.91351, 'container_id': 1},
            {'lat': 11.53855, 'lon': -72.91672, 'container_id': 2},
            {'lat': 11.54411, 'lon': -72.91564, 'container_id': 3},
            {'lat': 11.54987, 'lon': -72.90852, 'container_id': 4},
            {'lat': 11.55405, 'lon': -72.90532, 'container_id': 5},
            {'lat': 11.55119, 'lon': -72.90191, 'container_id': 6},
            {'lat': 11.54611, 'lon': -72.90792, 'container_id': 7}
        ]
    )
    distance: Optional[float] = 1933.2
    garbage_truck: int = Field(
        ...,
        gt=0,
        description='This is an Foreign Key in DB Schema. Possibly move this field to trip service model',
        example=21
    )



@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
async def home():
    return {"greeting": "Hello Garbage Service API"}



@app.post(
    path='/containers/new',
    response_model=Container,
    status_code=status.HTTP_201_CREATED
)
async def new_container(
    container: Container = Body(...)
):
    return container


@app.post(
    path='/route/new',
    response_model=Route,
    status_code=status.HTTP_201_CREATED
)
async def new_route(
    route: Route = Body(...)
):
    return route
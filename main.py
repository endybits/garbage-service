## Python
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
## Pydantic
from pydantic import BaseModel
from pydantic import Field

## FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Path

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
        ],
        default= [
            {'lat': 11.54752, 'lon': -72.91351, 'container_id': 1},
            {'lat': 11.53855, 'lon': -72.91672, 'container_id': 2},
            {'lat': 11.54411, 'lon': -72.91564, 'container_id': 3},
            {'lat': 11.54987, 'lon': -72.90852, 'container_id': 4},
            {'lat': 11.55405, 'lon': -72.90532, 'container_id': 5},
            {'lat': 11.55119, 'lon': -72.90191, 'container_id': 6},
            {'lat': 11.54611, 'lon': -72.90792, 'container_id': 7}
        ]
    )
    sorted_route: List[Dict[str, float]] = None
    distance: Optional[float] = 1933.2
    garbage_truck: int = Field(
        ...,
        gt=0,
        description='This is an Foreign Key in DB Schema. Possibly move this field to trip service model',
        example=21
    )


class TripGarbageService(BaseModel):
    date: datetime = None
    route_id: int = Field(
        ...,
        gt=0,
        example=11
    )
    truck_id: int = Field(
        ...,
        gt=0,
        example=22
    )


## ENDPOINTS
@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
async def home():
    return {"greeting": "Hello Garbage Service API"}


## Containers
@app.post(
    path='/containers/new',
    response_model=Container,
    status_code=status.HTTP_201_CREATED
)
async def new_container(
    container: Container = Body(...)
):
    return container


@app.get(
    path='/containers',
    #response_model=Container,
    status_code=status.HTTP_200_OK
)
async def container_resource_list():
    containers_location = [
        {'lat': 11.54752, 'lon': -72.91351, 'container_id': 1},
        {'lat': 11.53855, 'lon': -72.91672, 'container_id': 2},
        {'lat': 11.54411, 'lon': -72.91564, 'container_id': 3},
        {'lat': 11.54987, 'lon': -72.90852, 'container_id': 4},
        {'lat': 11.55405, 'lon': -72.90532, 'container_id': 5},
        {'lat': 11.55119, 'lon': -72.90191, 'container_id': 6},
        {'lat': 11.54611, 'lon': -72.90792, 'container_id': 7}
    ]
    container_list = []
    for base_container in containers_location:
        container = Container(
            volume=4000.0,
            latitude=base_container.get('lat'),
            longitude=base_container.get('lon')
        )
        container_dict = container.dict()
        container_dict.pop('status')
        container_list.append(container_dict)
    return {
        'result': container_list,
        'total_containers': len(container_list),
        'message': 'Container List'
    }

@app.put(
    path='/containers/{container_id}',
    status_code=status.HTTP_200_OK
)
async def upload_container(
    container_id: int = Path(
        ...,
        gt=0,
        title='Container ID',
        description='This field is the Container ID. It\'s required and must be greater than zero.',
        example=123
    ),
    container: Container = Body(...)
):
    return {
        'result': container,
        'message': 'Container Updated Successfully'
    }


@app.delete(
    path='/containers/{container_id}',
    status_code=status.HTTP_200_OK
)
async def remove_container(
    container_id: int = Path(
        ...,
        gt=0,
        title='Container ID',
        description='This field is the Container ID. It\'s required and must be greater than zero.',
        example=321
    )
):
    print(f"Deleting container with id... {container_id}")
    return {
        'result': {'pk':container_id},
        'message': 'Container Deleted Successfully'
    }


## Routes
@app.post(
    path='/route/new',
    response_model=Route,
    status_code=status.HTTP_201_CREATED
)
async def new_route(
    route: Route = Body(...)
):
    return route

@app.get(
    path='/route/{route_id}',
    status_code=status.HTTP_200_OK
)
async def view_route(
    route_id: int = Path(
        ...,
        gt=0,
        title='Route ID',
        description='This field is the Route ID to get a specific route. It\'s required and must be greater than zero.',
        example=444
    )
):
    route = Route(garbage_truck=555)
    route_dict = route.dict()
    return {
        'result': route_dict,
        'points': len(route_dict.get('route_list')),
        'message': 'Route Detail'
    }


@app.put(
    '/route/{route_id}/update/point/{container_id}',
    status_code=status.HTTP_200_OK
)
async def update_route_points(
    route_id: int = Path(
        ...,
        gt=0,
        title='Route ID',
        description='This field is the Route ID to update a specific route. It\'s required and must be greater than zero.',
        example=444
    ),
    container_id: int = Path(
        ...,
        gt=0,
        title='Container ID',
        description='This field allow us include the container location to the route. It\'s required and must be greater than zero.',
        example=321
    )
):
    container = Container(
        volume=4000.0,
        latitude=11.54611,
        longitude=-72.90792
    )
    route = Route(garbage_truck=555)
    container_point= {'lat': container.latitude, 'lon': container.longitude, 'container_id': container_id}
    route.route_list.append(container_point)
    
    return {
        'route': route,
        'route_points': len(route.route_list),
    }


@app.put(
    '/route/{route_id}/update',
    status_code=status.HTTP_200_OK
)
async def update_route(
    route_id: int = Path(
        ...,
        gt=0,
        title='Route ID',
        description='This field is the Route ID to update a specific route. It\'s required and must be greater than zero.',
        example=444
    ),
    route: Route = Body(...)
):  

    return {
        'route': route.dict(),
        'message': 'Route Updated Successfully'
    }


@app.delete(
    '/route/{route_id}',
    status_code=status.HTTP_200_OK
)
async def delete_route(
    route_id: int = Path(
        ...,
        gt=0,
        title='Route ID',
        description='This field is the Route ID to update a specific route. It\'s required and must be greater than zero.',
        example=444
    )
):  

    return {
        'route': route_id,
        'message': 'Route Deleted Successfully'
    }
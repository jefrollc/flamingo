import logging

from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from rich.logging import RichHandler
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import database

FORMAT = "%(asctime)s %(levelname)s %(name)-10s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="%d-%b %H:%M:%S",
    handlers=[RichHandler()],
)
logger = logging.getLogger("uvicorn")

app = FastAPI(title="flamingo")


@app.get("/", description="POL")
async def index():
    return {"ping": "pong"}


@asynccontextmanager
async def incrementer(prj):
    """Increment the Project's steps on exit"""
    yield
    prj.step = prj.step + 1
    await prj.save()


# Projects
@app.get(
    "/projects",
    response_model=List[database.Project],
    status_code=status.HTTP_200_OK,
    tags=["projects"],
    description="Get Projects",
)
async def get_projects():
    # Not sure how we catch an error when there are no records created.
    return await database.Project.from_queryset(database.ProjectORM.all())


@app.post(
    "/projects",
    response_model=database.Project,
    status_code=status.HTTP_201_CREATED,
    tags=["projects"],
    description="Create A Project",
)
async def create_projects(project: database.ProjectIn):
    project_obj = await database.ProjectORM.create(**project.dict(exclude_unset=True))
    return await database.Project.from_tortoise_orm(project_obj)


@app.put(
    "/projects/{project_id}",
    response_model=database.Project,
    status_code=status.HTTP_201_CREATED,
    tags=["projects"],
    description="Update A Project",
)
async def update_projects(project_id: int, project: database.ProjectIn):
    await database.ProjectORM.filter(id=project_id).update(
        **project.dict(exclude_unset=True)
    )
    return await database.Project.from_queryset_single(
        database.ProjectORM.get(id=project_id)
    )


@app.delete(
    "/projects/{project_id}",
    response_model=database.Status,
    status_code=status.HTTP_200_OK,
    tags=["projects"],
    description="Delete A Project",
)
async def delete_projects(project_id: int):
    if not (_ := await database.ProjectORM.get(id=project_id).delete()):
        raise HTTPException(status_code=404, detail="Project Not Found")
    return database.Status(message=f"{project_id} deleted")


@app.get(
    "/projects/{project_id}/items",
    response_model=List[database.Item],
    status_code=status.HTTP_200_OK,
    tags=["items"],
    description="Get Items for a Project",
)
async def get_project_items(project_id: int):
    return await database.Item.from_queryset(
        database.ItemORM.filter(project=project_id)
    )


@app.post(
    "/projects/{project_id}/items",
    response_model=List[database.ItemIn],
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    description="Add Items to a Project",
)
async def create_item(project_id: int, items: List[database.ItemIn]):
    p = await database.ProjectORM.get(id=project_id)
    async with incrementer(p):
        items_to_create = [
            database.ItemORM(**{**i.dict(), "project": p, "step": p.step})
            for i in items
        ]
        # XXX: These don't have `id`s here so we need to return `ItemIn`
        added_items = await database.ItemORM.bulk_create(
            items_to_create, ignore_conflicts=True
        )
    return [await database.ItemIn.from_tortoise_orm(i) for i in added_items]


@app.post(
    "/projects/{project_id}/items/known",
    response_model=List[database.Item],
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    description="Return items that are in the database",
)
async def get_known_items(project_id: int, keys: List[str]):
    p = await database.ProjectORM.get(id=project_id)
    items = database.ItemORM.filter(project=p, key__in=keys)
    return await database.Item.from_queryset(items)


@app.post(
    "/projects/{project_id}/items/unknown",
    response_model=List[str],
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    description="Return keys that are not the database",
)
async def get_unknown_items(project_id: int, keys: List[str]):
    p = await database.ProjectORM.get(id=project_id)
    known = {i.key for i in await database.ItemORM.filter(project=p, key__in=keys)}
    unknown = set(keys) - known
    return list(unknown)


register_tortoise(
    app,
    db_url=database.TORTOISE_ORM["connections"]["default"],
    modules={"models": ["database"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

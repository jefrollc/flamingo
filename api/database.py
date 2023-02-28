from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "sqlite://flamingo.db"},
    "apps": {
        "models": {
            "models": ["database", "aerich.models"],
            "default_connection": "default",
        },
    },
}
Tortoise.init_models(["__main__"], "models")


class ProjectORM(models.Model):
    """Project ORM"""

    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)
    name = fields.CharField(max_length=128, unique=True)
    description = fields.TextField(null=True)
    step = fields.IntField(default=0)
    # This is for random data we want associated with the project
    data = fields.JSONField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        table = "project"

    class PydanticMeta:
        exclude = ["created", "modified"]


class ItemORM(models.Model):
    """Item ORM"""

    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)
    key = fields.CharField(max_length=512, unique=True)
    # This groups INSERTS. Say you added some Items (step 1), then added some
    # more Items (step 2), then added some more items (step 3). After you
    # realized that you needed to remove the items inserted in step 2. This
    # makes it easier to do, as oppsed to writing something custom each time
    # you f-up. The name should prob be group but don't wanna interfear with
    # SQL keyword
    step = fields.IntField(default=0)
    # This is for random data we want associated with the key
    data = fields.JSONField(null=True)
    project = fields.ForeignKeyField(
        "models.ProjectORM",
        related_name="items",
        on_delete="CASCADE",
        null=True,
    )

    def __str__(self):
        return self.key

    class Meta:
        table = "item"
        indexes = [("project", "key")]

    class PydanticMeta:
        exclude = ["created", "modified"]


class Status(BaseModel):
    message: str


Project = pydantic_model_creator(ProjectORM, name="ProjectORM")
ProjectIn = pydantic_model_creator(
    ProjectORM, exclude=("step",), name="ProjectIn", exclude_readonly=True
)

Item = pydantic_model_creator(ItemORM, name="ItemORM")
ItemIn = pydantic_model_creator(
    ItemORM, exclude=("step",), name="ItemIn", exclude_readonly=True
)

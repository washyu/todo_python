from pydantic import BaseModel, ConfigDict

class ToDoBase(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class ToDoCreate(ToDoBase):
    pass

class ToDo(ToDoBase):
    id: int

    model_config = ConfigDict(from_attributes = True)
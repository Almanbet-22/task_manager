from pydantic import BaseModel, ConfigDict


class STaskBase(BaseModel):
    name: str
    description: str | None = None
    is_completed: bool = False

class STaskAdd(STaskBase):
    pass

class STask(STaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class STaskUpdate(STaskBase):
    name: str | None = None
    description: str | None = None
    is_completed: bool | None = None

class SUserRegister(BaseModel):
    email: str
    password: str

class SUserLogin(BaseModel):
    email: str
    password: str

class SUser(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
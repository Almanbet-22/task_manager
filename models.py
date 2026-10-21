from sqlalchemy import ForeignKey
from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship(back_populates="owner")

class Task(Model):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    is_completed: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="tasks")
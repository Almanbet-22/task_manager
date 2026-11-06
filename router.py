from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from database import SessionDep
from models import User, Task
from schemas import STask, STaskAdd, STaskUpdate
from typing import List
from auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task: STaskAdd, db: SessionDep, current_user: User = Depends(get_current_user)) -> STask:
    new_task = Task(**task.model_dump(), owner_id=current_user.id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/", status_code=status.HTTP_200_OK)
async def get_tasks(db: SessionDep, current_user: User = Depends(get_current_user)) -> List[STask]:
    result = await db.execute(select(Task).where(Task.owner_id == current_user.id))
    tasks = result.scalars().all()
    return tasks


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_task(id: int, db: SessionDep, current_user: User = Depends(get_current_user)) -> STask:
    result = await db.execute(select(Task).where(Task.id == id, Task.owner_id == current_user.id))
    task = result.scalars().first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Задача не найдена")
    return task


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_task(id: int, task: STaskUpdate, db: SessionDep, current_user: User = Depends(get_current_user)) -> STask:
    result = await db.execute(select(Task).where(Task.id == id, Task.owner_id == current_user.id))
    db_task = result.scalars().first()

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Задача не найдена")

    new_task = task.model_dump(exclude_unset=True)
    for key, value in new_task.items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int, db: SessionDep, current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == id, Task.owner_id == current_user.id))
    db_task = result.scalars().first()

    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Задача не найдена")

    await db.delete(db_task)
    await db.commit()
    return None

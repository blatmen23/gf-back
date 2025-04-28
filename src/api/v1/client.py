from fastapi import APIRouter
from typing import List

from src.schemas import Institute, Group, Student

router = APIRouter(tags=["Client"])

@router.get("/institutes")
async def institutes() -> List[Institute]:
    return [Institute(institute="ИАЭП", institute_num=3),
            Institute(institute="ФМФ", institute_num=2)]

@router.get("/groups")
async def groups() -> List[Group]:
    return []

@router.get("/students")
async def students() -> List[Student]:
    return []
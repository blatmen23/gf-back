from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import Institute, Group, Student
from .database import database as db
from .database import connection
from .models import (StudentsArchive,
                     ReportsArchive,
                     InstitutesTMP,
                     GroupsTMP,
                     StudentsTMP,
                     Institutes,
                     Groups,
                     Students,
                     InstitutesOld,
                     GroupsOld,
                     StudentsOld)


@connection
async def delete_all_tables(**kwargs):
    """
    This will not clear the student archive and archived report tables.
    """

    session: AsyncSession = kwargs['session']

    await session.execute(delete(InstitutesTMP))
    await session.execute(delete(GroupsTMP))
    await session.execute(delete(StudentsTMP))
    await session.execute(delete(Institutes))
    await session.execute(delete(Groups))
    await session.execute(delete(Students))
    await session.execute(delete(InstitutesOld))
    await session.execute(delete(GroupsOld))
    await session.execute(delete(StudentsOld))


@connection
async def insert_institutes_tmp(institutes: List[Institute], **kwargs):
    session: AsyncSession = kwargs['session']
    all_institutes: List[InstitutesTMP] = [InstitutesTMP(
        id=i.institute_num,
        institute=i.institute,
        institute_num=i.institute_num
    ) for i in institutes]
    session.add_all(all_institutes)


@connection
async def insert_groups_tmp(groups: List[Group], **kwargs):
    session: AsyncSession = kwargs['session']
    all_groups: List[GroupsTMP] = [GroupsTMP(
        id=g.group_id,
        group_=g.group,
        course=g.course,
        institute_id=g.institute_num
    ) for g in groups]
    session.add_all(all_groups)


@connection
async def insert_students_tmp(students: List[Student], **kwargs):
    session: AsyncSession = kwargs['session']
    all_groups: List[StudentsTMP] = [StudentsTMP(
        id=s.student_id,
        student=s.student,
        group_id=s.group_id,
        leader=s.leader
    ) for s in students]
    session.add_all(all_groups)

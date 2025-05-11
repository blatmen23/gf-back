from pprint import pprint
from typing import List
from src.schemas import Institute, Group, Student

from src.scraper.vendor import Scraper
from src.database import database_manager as db_m
from src.config import settings


async def run():
    scrapper = Scraper()
    try:
        await db_m.delete_all_tables()
        #
        # institutes = await scrapper.take_institutes()
        # await insert_institutes_tmp(institutes)
        # pprint(institutes)
        #
        # groups = await scrapper.take_groups()
        # await insert_groups_tmp(groups)
        # pprint(groups)
        # async for students_chunk in scrapper.take_students():
        #     await insert_students_tmp(students_chunk)
        #     pprint(students_chunk)
    except Exception as e:
        raise e

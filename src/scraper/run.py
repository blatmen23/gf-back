from pprint import pprint
from typing import List
from src.schemas import Institute, Group, Student

from src.scraper.vendor import Scraper
from src.config import settings


async def run():
    scrapper = Scraper()
    try:
        institutes = await scrapper.take_institutes()
        pprint(institutes)
        groups = await scrapper.take_groups()
        pprint(groups)
        async for students_chunk in scrapper.take_students():
            ...
            # pprint(students_chunk)
    except Exception as e:
        raise e

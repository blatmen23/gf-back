import asyncio
from json import loads
from pprint import pprint
from collections import deque
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
from aiohttp import ClientSession, ClientResponse, ClientTimeout
from functools import wraps
from typing import AsyncGenerator, Generator, List

from src.config import settings
from src.schemas import Institute, Group, Student


def aiohttp_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        connector = ProxyConnector.from_url(url=str(settings.proxy.url))
        timeout = ClientTimeout(total=settings.scraper.connection_timeout)

        async with ClientSession(
                trust_env=True,
                timeout=timeout,
                connector=connector
        ) as session:
            kwargs['session'] = session
            return await func(*args, **kwargs)

    return wrapper


class Scraper:
    def __init__(self):
        self.institutes: List[Institute] = []
        self.groups: deque[Group] = deque()

        self.exception_counter = 0
        self.recursions_count = 0

    @staticmethod
    def get_random_headers():
        return {
            'Accept': 'text/html,application/xhtml+xml,'
                      'application/xml;q=0.9,image/avif,image/webp,'
                      'image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.7',
            'User-Agent': UserAgent().random,
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control:': 'max-age=0'
        }

    async def take_institutes(self):
        self.institutes = [Institute(institute_num=i) for i in range(1, 7)]
        return self.institutes

    @aiohttp_session
    async def take_groups(self, session: ClientSession) -> List[Group]:
        url = "https://kai.ru/web/studentu/raspisanie1"
        params = {
            "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
            "p_p_lifecycle": 2,
            "p_p_state": "normal",
            "p_p_mode": "view",
            "p_p_resource_id": "getGroupsURL",
            "p_p_cacheability": "cacheLevelPage",
            "p_p_col_id": "column-1",
            "p_p_col_count": 1
        }
        try:
            response: ClientResponse = await session.get(url=url,
                                                         params=params,
                                                         headers=self.get_random_headers())
            groups_data = loads(await response.text())[0:36:1]

            for group_data in groups_data:
                institute_num = int(
                    "1" if group_data['group'].startswith('8') else
                    group_data['group'][0])
                self.groups.append(
                    Group(
                        group_id=group_data['id'],
                        group=group_data['group'],
                        course=group_data['group'][1],
                        institute_num=institute_num
                    )
                )
        except asyncio.TimeoutError:
            print(f"Recursion parsing groups {self.recursions_count}: ")
            if self.recursions_count > settings.scraper.recursion_limit:
                raise f"The recursion limit has been reached: {self.recursions_count}"
            else:
                print("TimeoutError in get_groups query\n")
                await asyncio.sleep(settings.scraper.time_delta_after_exception)
                self.recursions_count += 1
                await self.take_groups()
        else:
            self.recursions_count = 0
        return list(self.groups)

    @aiohttp_session
    async def get_students_from_group(self, session: ClientSession,
                                      group: Group) -> List[Student]:
        url = "https://kai.ru/infoClick/-/info/group"
        params = {
            "id": group.group_id,
            "name": group.group
        }
        students: List[Student] = []
        try:
            response: ClientResponse = await session.get(url=url,
                                                         params=params,
                                                         headers=self.get_random_headers())
            group_page = await response.text()
            soup = BeautifulSoup(group_page, "html.parser")

            table = soup.find("tbody")
            if table is None:
                alert = soup.find("div", class_="alert alert-info")
                if alert is None:
                    print("table tag is NoneType, why?", group.group)
                    self.groups.append(group)
                    self.exception_counter += 1
                    print(list(self.groups)[-1])
                    return
                else:
                    print(group.group, "is", alert.text)
                    return

            trows = table.find_all("tr")
            for trow in trows:
                tcolumns = trow.find_all("td")
                student_column = tcolumns[1]
                student = student_column.find(text=True,
                                              recursive=False).get_text(
                    strip=True)
                leader = True if student_column.find(
                    "span") is not None else False
                students.append(
                    Student(
                        student=student,
                        group_id=group.group_id,
                        leader=leader
                    )
                )
        except asyncio.TimeoutError:
            self.groups.append(group)
            self.exception_counter += 1
            print(list(self.groups)[-1])
            print(
                f"TimeoutError in group: id->{group.group_id} group->{group.group}")
            print(f"groups in groups_queue: {len(self.groups)}")
        return students

    def get_groups_pool(self) -> Generator[List[Group], None, None]:
        group_chunk: List[Group] = []
        while self.groups:  # Пока в deque есть элементы
            group = self.groups.popleft()  # Извлекаем элемент из начала deque
            group_chunk.append(group)
            if (len(group_chunk) == settings.scraper.max_pool_size) or not self.groups:
                yield group_chunk
                group_chunk = []

    async def take_students(self):
        for groups_pool in self.get_groups_pool():
            res = await asyncio.gather(
                *[self.get_students_from_group(group=group) for group in
                  groups_pool])  # [[1, 2], [], [3, 2], [0, 23, 4], [], []]

            if self.exception_counter > settings.scraper.max_exception_counter:
                raise "self.exception_counter more than 100!"

            students = []  # [1, 2, 3, 2, 0, 23, 4]
            for r_list in res:
                if not r_list:
                    continue
                for r in r_list:
                    students.append(r)

            print(f"\nreturned {len(students)} students")
            print(f"groups in queue: {len(self.groups)}, "
                  f"exception_counter={self.exception_counter}/{settings.scraper.max_exception_counter}")

            yield students
            await asyncio.sleep(settings.scraper.time_delta)
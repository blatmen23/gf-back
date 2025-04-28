from pydantic import BaseModel

class Group(BaseModel):
    group_id: int
    group: str
    course: int
    institute_num: int

from hashlib import sha1
from pydantic import BaseModel, Field, computed_field

class Student(BaseModel):
    student: str
    group_id: int
    leader: bool = Field(default=False)

    @computed_field(return_type=int)  # type: ignore[prop - decorator]
    @property
    def student_id(self):
        hex_hash = sha1(self.student.encode("utf-8")).hexdigest()
        int_hash = int(hex_hash, 16)
        return int_hash % 10_000_000


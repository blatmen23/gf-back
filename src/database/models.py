import datetime
from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import JSON
from sqlalchemy import func, ForeignKey

class Base(DeclarativeBase):
    type_annotation_map = {
        dict: JSON
    }

    date: Mapped[datetime.datetime] = mapped_column(default=func.now())

class ReportsArchive(Base):
    __tablename__ = "reports_archive"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_content: Mapped[str]
    report_json: Mapped[dict]

class StudentsArchive(Base):
    __tablename__ = "students_archive"

    id: Mapped[int] = mapped_column(primary_key=True)
    institute: Mapped[str] = mapped_column(nullable=False)
    course: Mapped[int] = mapped_column(nullable=False)
    group_: Mapped[int] = mapped_column(nullable=False)
    student: Mapped[str] = mapped_column(nullable=False)

# --------------------

class Institutes(Base):
    __tablename__ = "institutes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    institute: Mapped[str] = mapped_column(nullable=False)
    institute_num: Mapped[int] = mapped_column(nullable=False)

    groups: Mapped[List["Groups"]] = relationship(back_populates="institutes")

class Groups(Base):
    __tablename__ = "groups_"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    group_: Mapped[str] = mapped_column(nullable=False, autoincrement=False)
    course: Mapped[int] = mapped_column(nullable=False)
    institute_id: Mapped[int] = mapped_column(ForeignKey("institutes.id", ondelete="CASCADE"))

    institutes: Mapped["Institutes"] = relationship(back_populates="groups_")
    students: Mapped[List["Groups"]] = relationship(back_populates="groups_")


class Students(Base):
    __tablename__ = "students"
    # id теперь это ФИО студента
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    student: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups_.id", ondelete="CASCADE"))
    leader: Mapped[bool] = mapped_column(default=False)

    groups: Mapped["Groups"] = relationship(back_populates="students")

# --------------------

class OldInstitutes(Base):
    __tablename__ = "old_institutes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    institute: Mapped[str] = mapped_column(nullable=False)
    institute_num: Mapped[int] = mapped_column(nullable=False)

    groups: Mapped[List["OldGroups"]] = relationship(back_populates="old_institutes")

class OldGroups(Base):
    __tablename__ = "old_groups_"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    group_: Mapped[str] = mapped_column(nullable=False, autoincrement=False)
    course: Mapped[int] = mapped_column(nullable=False)
    institute_id: Mapped[int] = mapped_column(ForeignKey("old_institutes.id", ondelete="CASCADE"))

    institutes: Mapped["OldInstitutes"] = relationship(back_populates="old_groups_")
    students: Mapped[List["OldStudents"]] = relationship(back_populates="old_groups_")

class OldStudents(Base):
    __tablename__ = "old_students"

    # id теперь это ФИО студента
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    student: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("old_groups_.id", ondelete="CASCADE"))
    leader: Mapped[bool] = mapped_column(default=False)

    groups: Mapped["OldGroups"] = relationship(back_populates="old_students")
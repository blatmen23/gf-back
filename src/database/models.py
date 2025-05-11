from datetime import datetime
from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import JSON
from sqlalchemy import func, ForeignKey

class Base(DeclarativeBase):
    type_annotation_map = {
        dict: JSON
    }

    created_at: Mapped[datetime] = mapped_column(default=func.now())

# --------------------

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

class InstitutesTMP(Base):
    __tablename__ = "institutes_tmp"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    institute: Mapped[str] = mapped_column(nullable=False)
    institute_num: Mapped[int] = mapped_column(nullable=False)

    groups: Mapped[List["GroupsTMP"]] = relationship(back_populates="institute")

class GroupsTMP(Base):
    __tablename__ = "groups_tmp"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    group_: Mapped[str] = mapped_column(nullable=False, autoincrement=False)
    course: Mapped[int] = mapped_column(nullable=False)
    institute_id: Mapped[int] = mapped_column(ForeignKey("institutes_tmp.id", ondelete="CASCADE"))

    institute: Mapped["InstitutesTMP"] = relationship(back_populates="groups")
    students: Mapped[List["StudentsTMP"]] = relationship(back_populates="group_")


class StudentsTMP(Base):
    __tablename__ = "students_tmp"
    # id теперь это хеш от ФИО студента
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    student: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups_tmp.id", ondelete="CASCADE"))
    leader: Mapped[bool] = mapped_column(default=False)

    group_: Mapped["GroupsTMP"] = relationship(back_populates="students")

# --------------------

class Institutes(Base):
    __tablename__ = "institutes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    institute: Mapped[str] = mapped_column(nullable=False)
    institute_num: Mapped[int] = mapped_column(nullable=False)

    groups: Mapped[List["Groups"]] = relationship(back_populates="institute")

class Groups(Base):
    __tablename__ = "groups_"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    group_: Mapped[str] = mapped_column(nullable=False, autoincrement=False)
    course: Mapped[int] = mapped_column(nullable=False)
    institute_id: Mapped[int] = mapped_column(ForeignKey("institutes.id", ondelete="CASCADE"))

    institute: Mapped["Institutes"] = relationship(back_populates="groups")
    students: Mapped[List["Students"]] = relationship(back_populates="group_")


class Students(Base):
    __tablename__ = "students"
    # id теперь это хеш от ФИО студента
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    student: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups_.id", ondelete="CASCADE"))
    leader: Mapped[bool] = mapped_column(default=False)

    group_: Mapped["Groups"] = relationship(back_populates="students")

# --------------------

class InstitutesOld(Base):
    __tablename__ = "institutes_old"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    institute: Mapped[str] = mapped_column(nullable=False)
    institute_num: Mapped[int] = mapped_column(nullable=False)

    groups: Mapped[List["GroupsOld"]] = relationship(back_populates="institute")

class GroupsOld(Base):
    __tablename__ = "groups_old"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    group_: Mapped[str] = mapped_column(nullable=False, autoincrement=False)
    course: Mapped[int] = mapped_column(nullable=False)
    institute_id: Mapped[int] = mapped_column(ForeignKey("institutes_old.id", ondelete="CASCADE"))

    institute: Mapped["InstitutesOld"] = relationship(back_populates="groups")
    students: Mapped[List["StudentsOld"]] = relationship(back_populates="group_")


class StudentsOld(Base):
    __tablename__ = "students_old"
    # id теперь это хеш от ФИО студента
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    student: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups_old.id", ondelete="CASCADE"))
    leader: Mapped[bool] = mapped_column(default=False)

    group_: Mapped["GroupsOld"] = relationship(back_populates="students")
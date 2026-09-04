import typing
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class NutrientUnit(StrEnum):
    GRAMM = "g"
    MILLI_GRAMM = "mg"
    MICRO_GRAMM = "ug"


class Micronutrient(Base):
    __tablename__ = "micronutrient"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    recommended_daily_amount: Mapped[float]
    unit: Mapped[NutrientUnit] = mapped_column(
        Enum(NutrientUnit, values_callable=lambda x: [i.value for i in x])
    )

    __mapper_args__: typing.ClassVar = {"polymorphic_identity": "micronutrient"}


class VitaminGroup(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    K = "K"


class Vitamin(Micronutrient):
    __tablename__ = "vitamin"
    micronutrient_id: Mapped[uuid4] = mapped_column(
        ForeignKey("micronutrient.id"), primary_key=True
    )
    vitamin_group: Mapped[VitaminGroup] = mapped_column(
        Enum(VitaminGroup, values_callable=lambda x: [i.value for i in x])
    )

    __mapper_args__: typing.ClassVar = {"polymorphic_identity": "vitamin"}

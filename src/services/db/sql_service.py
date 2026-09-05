from uuid import UUID

from sqlalchemy import func, select

from src.services.db.db_models import Vitamin
from src.services.db.engine import SessionLocal


def insert_vitamine(vitamin: dict | Vitamin) -> UUID:
    """
    BEGIN;
        WITH inserted AS (
            INSERT INTO micronutrient VALUES ('9b15bb9c-2c09-4bc3-8059-bd5667727592', 'B8', '10', 'mg')
            RETURNING id
        )
        INSERT INTO vitamin (micronutrient_id, vitamin_group) SELECT id, 'B' FROM inserted;
    COMMIT;
    """
    with SessionLocal.begin() as session:
        vitamin = Vitamin(**vitamin) if isinstance(vitamin, dict) else vitamin
        session.add(vitamin)
        session.flush()  # vitamin entity is inserted in db (not yet commited) and id is assigned to vitamin.id
        return vitamin.id


def get_vitamin(id: UUID) -> Vitamin:
    """
    SELECT * FROM vitamin
    INNER JOIN micronutrient ON micronutrient.id = vitamin.micronutrient_id
    WHERE id = $'id'
    """
    with SessionLocal() as session:
        vitamin = session.get(Vitamin, id)
        return vitamin


def get_vitamin_by_name(name: str) -> Vitamin | None:
    """
    SELECT * FROM vitamin
    INNER JOIN micronutrient ON micronutrient.id = vitamin.micronutrient_id
    WHERE name = $'name'
    """
    with SessionLocal() as session:
        stmt = select(Vitamin).where(func.lower(Vitamin.name) == name.lower())
        vitamin = session.scalars(stmt).first()
        return vitamin


if __name__ == "__main__":
    b12g = get_vitamin(id="9b15bb9c-2c09-4bc3-8059-bd5667727596")
    print(b12g)
    b12g = get_vitamin_by_name(name="b12")
    print(b12g)
    # vitamin = Vitamin(
    #     name="B12", recommended_daily_amount=10, unit="mg", vitamin_group="B"
    # )
    # b12 = insert_vitamine(vitamin=vitamin)
    # vitamin_retinoide = Vitamin(
    #     name="Retinoide", recommended_daily_amount=850, unit="ug", vitamin_group="A"
    # )
    # retionoide = insert_vitamine(vitamin=vitamin_retinoide)
    # vitamin_carotinoide = Vitamin(
    #     name="Provitamin-A-Carotinoide",
    #     recommended_daily_amount=850,
    #     unit="ug",
    #     vitamin_group="A",
    # )
    # carotinoide = insert_vitamine(vitamin=vitamin_carotinoide)
    # print(b12, retionoide, carotinoide)

from src.services.db.db_models import Vitamin
from src.services.db.engine import SessionLocal


def insert_vitamine(vitamin: dict | Vitamin):
    with SessionLocal.begin() as session:
        vitamin = Vitamin(**vitamin) if isinstance(vitamin, dict) else vitamin
        session.add(vitamin)


if __name__ == "__main__":
    vitamin = Vitamin(
        name="B12", recommended_daily_amount=10, unit="mg", vitamin_group="B"
    )
    insert_vitamine(vitamin=vitamin)
    vitamin_retinoide = Vitamin(
        name="Retinoide", recommended_daily_amount=850, unit="ug", vitamin_group="A"
    )
    insert_vitamine(vitamin=vitamin_retinoide)
    vitamin_carotinoide = Vitamin(
        name="Provitamin-A-Carotinoide",
        recommended_daily_amount=850,
        unit="ug",
        vitamin_group="A",
    )
    insert_vitamine(vitamin=vitamin_carotinoide)

# Micronutrients

Micronutrients is a containerized Python backend project focused on relational database design and REST API development.

The database is designed using an **Entity-Relationship Model (ERM)**, transformed into a relational data model, and implemented as a physical **PostgreSQL** schema.  
The backend is built with **FastAPI**, with **SQLAlchemy** providing the ORM and database access layer and **Alembic** handling version-controlled schema migrations.  
**Docker Compose** is used to orchestrate the services and provide a reproducible development environment.  
**Unit and integration tests** are implemented with **pytest** to validate the application and its database interactions.

## Data modelling

### ER-Modell

> ![NOTE]
> The original drawio file can be found inside [./assets/data_modelling/micro_nutrition_erm.drawio](./assets/data_modelling/micro_nutrition_erm.drawio)

![Entity-Relation-Modell](./assets/data_modelling/micro_nutrition_erm.drawio.svg)

# Micronutrients 🥦📊🧬

Micronutrients is a containerized **Python** backend project focused on **relational database design** and **REST API** development for persisting, manipulating and retrieving information about micronutrients.

The database is designed using an **Entity-Relationship Model (ERM)**, transformed into a relational data model, and implemented as a physical **PostgreSQL** schema.  
The backend is built with **FastAPI**, with **SQLAlchemy** providing the ORM and database access layer and **Alembic** handling version-controlled schema migrations.  
**Docker Compose** is used to orchestrate the services and provide a reproducible development environment.  
**Unit and integration tests** are implemented with **pytest** to validate the application and its database interactions.

## Data modelling

### ER-Modell (Conceptual)

> [!NOTE]
> The original drawio file can be found inside [./assets/data_modelling/micro_nutrition_erm.drawio](./assets/data_modelling/micro_nutrition_erm.drawio)

![Entity-Relation-Modell](./assets/data_modelling/micro_nutrition_erm.drawio.svg)

### Relation Modell (Logical)

#### Unoptimized

Symptom(<u>id</u>, name, category)
Micronutrient(<u>id</u>, name, recommended_daily_amount, unit)  
NutrientImproveSymptom(<u>↑ micronutrientId</u>, <u>↑ symptomId</u>)  
Vitamin(<u>↑ micronutrientId</u>, group, fat_soluble)  
FoodCategory(<u>id</u>, name, description)  
Food(<u>id</u>, name, description)  
FoodHasCategory(<u>↑ foodId</u>, foodCategoryId)  
FoodConsistsOfNutrient(<u>↑ foodId</u>, <u>↑ micronutrientId</u>, amount, unit, per_quantity)

#### Optimized

Symptom(<u>id</u>, name, category)
Micronutrient(<u>id</u>, name, recommended_daily_amount, unit)  
NutrientImproveSymptom(<u>↑ micronutrientId</u>, <u>↑ symptomId</u>)  
Vitamin(<u>↑ micronutrient_id</u>, group, fat_soluble)  
FoodCategory(<u>id</u>, name, description)  
Food(<u>id</u>, name, description, ↑ foodCategoryId) *Added foodCategoryId\*  
~~FoodHasCategory(<u>↑ foodId</u>, foodCategoryId)~~  
FoodConsistsOfNutrient(<u>↑ foodId</u>, <u>↑ micronutrientId</u>, amount, unit, per*quantity)

### PostgreSQL Modell (Physical)

> [!IMPORTANT]
> Some improvements:
>
> - Names for tables and columns are lower and snake case
> - `vitamin.fat_soluble` is not persisted for now because it is an vitamin group property which cannot be modelled so far since `vitamin_group` is only an enum.

```sql
CREATE TYPE symptom_category AS ENUM ('outer', 'inner');

CREATE TABLE symptom (
    id UUID NOT NULL,
    name VARCHAR(50) NOT NULL,
    category symptom_category NOT NULL,
    PRIMARY KEY (id)
);

CREATE TYPE nutrient_unit AS ENUM ('mg', 'ug', 'g');

CREATE TABLE micronutrient (
    id UUID NOT NULL,
    name VARCHAR(50) NOT NULL,
    recommended_daily_amount DECIMAL(10,3),
    unit nutrient_unit,

    PRIMARY KEY (id),
    CHECK (
        (recommended_daily_amount IS NULL AND unit IS NULL)
        OR
        (
            recommended_daily_amount IS NOT NULL
            AND recommended_daily_amount > 0
            AND unit IS NOT NULL
        )
    )

);

CREATE TABLE nutrient_improves_symptom (
    micronutrient_id UUID NOT NULL,
    symptom_id UUID NOT NULL,
    PRIMARY KEY (micronutrient_id, symptom_id),
    FOREIGN KEY (micronutrient_id) REFERENCES micronutrient(id),
    FOREIGN KEY (symptom_id) REFERENCES symptom(id)
);

CREATE TYPE vitamin_group AS ENUM ('A', 'B', 'C', 'D', 'E', 'K');

CREATE TABLE vitamin (
    micronutrient_id UUID NOT NULL,
    vitamin_group vitamin_group NOT NULL,

    PRIMARY KEY (micronutrient_id),
    FOREIGN KEY (micronutrient_id) REFERENCES micronutrient(id)
);

CREATE TABLE food_category (
    name VARCHAR(50) NOT NULL,
    description TEXT,
    PRIMARY KEY (name)
);

CREATE TABLE food (
    id UUID NOT NULL,
    name VARCHAR(50) NOT NULL,
    food_category_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (food_category_name) REFERENCES food_category(name)
);

CREATE TYPE food_unit AS ENUM ('g', 'kg', 'ml', 'l', 'piece', 'portion');

CREATE TABLE food_consists_of_nutrient (
    food_id UUID NOT NULL,
    micronutrient_id UUID NOT NULL,
    nutrient_amount DECIMAL(10,3), -- this and following attributes can be null
    nutrient_unit nutrient_unit,
    food_amount DECIMAL(10,3),
    food_unit food_unit,

    PRIMARY KEY (food_id, micronutrient_id),
    FOREIGN KEY (food_id) REFERENCES food(id),
    FOREIGN KEY (micronutrient_id) REFERENCES micronutrient(id),

    CHECK (nutrient_amount > 0),
    CHECK (food_amount > 0)
);
```

## Docker environment

### PostgreSQL

We use docker / docker-compose to set up the PostgreSQL database. The container runs with the latest `postgres:18.6` version.

> [!NOTE]
> For interacting with the database in the beginning we use [`adminer`](https://www.adminer.org/de/) as postgres client. The reason for this is that is also used on the offical postgres docker documentation. As alternative we could have also used [`pgadmin`](https://www.pgadmin.org/).

> [!NOTE]
> How to find the name of the network? Per default it is called `<Docker-compose-projectname>_default`:
>
> - `docker network ls`
> - `docker compose config` shows the optimized docker-compose.yml file.
> - `docker inspect postgres` search for `networks`

> [!NOTE]
> Use a _Named Volume_ instead of a _Bind mount_. When using _Named Volume_:
>
> - Docker cares about the persisting
> - less issues with windows / linux file permissions
> - No dependency on specific file paths

> [!NOTE]
> The docker compose file can be checked [here](docker-compose.yml) or inside the src directory via `docker compose config`.

### Data schema migration

#### Local environment

```sh
pip install --upgrade uv

uv init

uv add --group migration alembic
uv add --group migration psycopg[binary]

uv run alembic init migrations
```

Inside _alembic.ini_ set `sqlalchemy.url=`. Set the database URL as environment variable. Inside _env.py_ import the environment variable and asign it to `config.set_main_option("sqlalchemy.url", database_url)`.

> [!IMPORTANT]
> When you run locally in a virtual environment and your postgres instance is running inside a container the container has to expose the port and inside the `sqlalchemy.url=` you define `...@localhost:<PORT>/<DATABASE>`.

```sh
# Create first revision
uv run alembic revision -m "create symptom_category enum type"
```

Define the revision with `upgrade` and `downgrade` functionalities. In this case we define an Enum type for the symptom category and we drop it in case of a rollback.

```sh
# Apply revision
uv run alembic upgrade head
```

#### Pack it into a container with docker run

Create following Dockerfile.

```Dockerfile
FROM python:3.13-alpine AS migration
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen --group migration

COPY migrations migrations
COPY alembic.ini .

ENTRYPOINT ["uv", "run", "alembic"]
# ENTRYPOINT cannot be overwritten but you can extend
CMD ["upgrade", "head"]
# CMD will be completely overwritten (in this case CMD is like a default value)
```

```sh
# Build image
docker build -t migration-img .

# Run container
# micronutrients_default is the network which is created automatically by docker-compose when environment is started
docker run --rm --name migration -e DATABASE_URL="postgresql+psycopg://user:pw@postgresdb:5432/pdb" --network micronutrients_default migration-img
```

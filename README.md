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

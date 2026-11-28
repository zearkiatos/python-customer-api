from sqlalchemy.engine import Engine
from sqlmodel import SQLModel


def initialize_sqlite_schema(engine: Engine) -> None:
    with engine.connect() as connection:
        # Serialize the schema check and change across workers.
        connection.exec_driver_sql("BEGIN IMMEDIATE")
        SQLModel.metadata.create_all(connection)
        columns = connection.exec_driver_sql("PRAGMA table_info(customer_plans)").all()
        if "state" not in {column.name for column in columns}:
            connection.exec_driver_sql(
                "ALTER TABLE customer_plans ADD COLUMN state VARCHAR NOT NULL DEFAULT 'ACTIVE'"
            )
        connection.commit()

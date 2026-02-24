# 3. Using alembic to manage database changes

In this app you will use SQLModel (or SQLAlchemy if you prefer) to interact with the SQLite
database.

In COMP0035 you learned how to create the database tables using classes that inherited the SQLModel
class.

You have been given model classes in models/models.py. This is a modified version of the code
from COMP0035.

During the project you may need to make changes to the model classes and update the database. The
recommended approach to manage these changes is to use `alembic`, a Python library for managing
migrations.

Complete the following steps to set up and use alembic for the tutorial project.

1. Install `alembic`. This was installed when you set up the project. If you skipped the project
   setup then install now: `pip install alembic`
2. Initialise alembic for the project: `alembic init alembic`. This will install in the project root
   a folder called `alembic` and a file called `alembic.ini`.
3. Configure `alembic.ini`:
    - Open the file and set the `sqlalchemy.url` to:
      
      `sqlalchemy.url = sqlite:///%(here)s/src/data/paralympics.db`
    
      `%(here)s` is a placeholder that expands to the directory containing the INI file.
4. Configure `alembic/env.py`. Edit the `add your model's MetaData object here` and edit it to match
   the following. You may prefer to just copy all the following and replace the contents of env.py:
   ```python
    from logging.config import fileConfig
    from sqlalchemy import engine_from_config
    from sqlalchemy import pool
    from alembic import context
    
    # this is the Alembic Config object, which provides access to the values within the .ini file in use.
    config = context.config
    
    # Interpret the config file for Python logging. This line sets up loggers basically.
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)
    
    # add your model's MetaData object here for 'autogenerate' support
    # from myapp import mymodel
    # target_metadata = mymodel.Base.metadata
    import sys
    import os
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))  # Add project root to sys.path
    from backend.models.models import GamesHost, GamesDisability, GamesTeam, Games, Team, Disability, Host, Country, Question, Response # noqa
    from sqlmodel import SQLModel
    target_metadata = SQLModel.metadata
    
    # This is a common naming convention dictionary
    naming_convention = {
            "ix": "ix_%(table_name)s_%(column_0_label)s",  # Added table_name for more uniqueness
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",  # Used constraint_name for check constraints
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        }
    
    def run_migrations_offline() -> None:
        """Run migrations in 'offline' mode.
    
        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well.  By skipping the Engine creation
        we don't even need a DBAPI to be available.
    
        Calls to context.execute() here emit the given string to the
        script output.
    
        """
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            compare_type=True,  # Detects column type changes
            naming_convention=naming_convention,  # Add naming convention
            render_as_batch=True  # Enable batch mode, crucial for SQLite
        )
    
        with context.begin_transaction():
            context.run_migrations()
    
    
    def run_migrations_online() -> None:
        """Run migrations in 'online' mode.
    
        In this scenario we need to create an Engine
        and associate a connection with the context.
    
        """
    
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,  # Detects column type changes
                naming_convention=naming_convention,  # Add naming convention
                render_as_batch=True  # Enable batch mode, crucial for SQLite
            )
    
            with context.begin_transaction():
                context.run_migrations()
    
    
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
   ```
5. Create the initial migration: `alembic revision -m "1_create_initial_tables" --autogenerate`
6. Apply the migration to create the database with tables: `alembic upgrade head`
7. Any time you make changes to database table models in `models.py` you generate a new migration
   and upgrade the head using these two steps:
    - `alembic revision -m "add_date_to_games" --autogenerate`
    - `alembic upgrade head`

### Further guidance on using alembic

- [Alembic official tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Alembic with SQLModel tutorials](https://dev.to/mchawa/sqlmodel-alembic-tutorial-gc8) this was
  used for the `env.py` given above.

[Next activity](4-database.md)
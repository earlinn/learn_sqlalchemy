from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from config import settings
from database import Base
from models import WorkersORM  # noqa

# если импортировать только Base и не импортировать модели, то Base будет пустой,
# т.е. в нем не будет информации о дочерних классах
# мы добавили комментарий noqa, чтобы линтер не ругался и не стер неиспользуемый импорт

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# поменяли переменную sqlalchemy.url из alembic.ini на наше асинхронное подключение к БД
# таким же способом можно поменять любые другие переменные из файла alembic.ini
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url_asyncpg + "?async_fallback=True",
)

# в target_metadata передаются все наши модели данных (таблицы)
target_metadata = Base.metadata


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
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

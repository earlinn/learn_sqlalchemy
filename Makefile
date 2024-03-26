alembic-init:
	alembic init src/migrations

# чтобы получилось, как в видео, нужно в файле .env указать название нашей пустой БД
# (sa_alembic), но у меня все равно создавалась пустая миграция, хотя я удалила весь
# pycache из всех папок и подпапок, потом я в файле config.py вывела название БД
# на печать (позже удалила этот принт), и тогда у меня создалась не пустая миграция,
# а все как на видео, а в pgadmin4 у БД sa_alembic появилась таблица alembic_version
makemig:
	alembic revision --autogenerate

makemig-named:
	alembic revision --autogenerate -m "migration 2"

# создать файл с пустой миграцией, которую затем можно заполнить вручную
makemig-empty:
	alembic revision

migrate:
	alembic upgrade head

undo-all-migrations:
	alembic downgrade base

# вставить номер миграции, до которой надо откатиться
undo-migrations:
	alembic downgrade f111dde6790b
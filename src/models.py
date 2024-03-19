from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# declarative mapping style
class WorkersORM(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

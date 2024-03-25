from datetime import datetime

from pydantic import BaseModel

from models import WorkLoad

# DTO- data transfer object, класс, который передает данные между слоями (сервисами)
# приложения и больше ничего не делает. Данные, которые отдает нам Алхимия, не очень
# удобны для работы, поэтому нам нужно привести их к нужной нам структуре

# принято сначала писать класс для POST-запросов, а потом от него наследовать класс
# для GET-запросов, который уже будет включать все поля


class WorkersPostDTO(BaseModel):
    username: str


class WorkersDTO(WorkersPostDTO):
    id: int


class CVsPostDTO(BaseModel):
    title: str
    compensation: int | None
    workload: WorkLoad
    worker_id: int


class CVsDTO(CVsPostDTO):
    id: int
    created_at: datetime
    updated_at: datetime


class CVsRelationshipDTO(CVsDTO):
    worker: "WorkersDTO"


class WorkersRelationshipDTO(WorkersDTO):
    cvs: list["CVsDTO"]


class VacanciesPostDTO(BaseModel):
    title: str
    compensation: int | None


class VacanciesDTO(VacanciesPostDTO):
    id: int


class CVsRelationshipVacanciesRepliedDTO(CVsDTO):
    worker: "WorkersDTO"
    vacancies_replied: list["VacanciesDTO"]

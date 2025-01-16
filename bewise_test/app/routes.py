from fastapi import APIRouter, Depends

from app.db.repos import ApplicationRepo
from app.deps import get_sqla_repo, get_service
from app.documenters import Q
from app.schemas import ApplicationSchema
from app.service import ApplicationService

router = APIRouter()

@router.post("/applications")
async def create_application(intake: ApplicationSchema, service: ApplicationService = Depends(get_service)):
    """
    Разместить заявку
    """
    return await service.create_application(intake)

@router.get("/applications")
async def get_applications(
    repo: ApplicationRepo = Depends(get_sqla_repo(ApplicationRepo)),
    user_name: str = Q('username', None, description='filter aapplications by username'),
    page: int = Q('page', 1, description='page'),
    page_size: int = Q("page size", 10, description="page_size"),
):
    """
    Получить список заявок
    """
    return await repo.get_many(user_name, page, page_size)
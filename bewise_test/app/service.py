from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repos import ApplicationRepo
from app.messages import KafkaPublisher
from app.models import Application
from app.schemas import ApplicationSchema


class ApplicationService:

    def __init__(
        self, session: AsyncSession, message_publisher: KafkaPublisher
    ) -> None:
        self.session = session
        self.applications = ApplicationRepo(session)
        self.messages = message_publisher

    async def create_application(self, intake: ApplicationSchema):
        model = Application.model_validate(intake.model_dump())
        await self.applications.create(model)
        await self.session.commit()
        await self.messages.publish_message(model)
        return model

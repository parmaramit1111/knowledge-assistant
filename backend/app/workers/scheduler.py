
import asyncio

from app.core.config import settings
from app.workers.document.document_worker import DocumentWorker


class WorkerScheduler:

    def __init__(self) -> None:
        self.document_worker = DocumentWorker()

    async def start(self) -> None:

        while settings.worker_enabled:

            await self.document_worker.run()

            await asyncio.sleep(
                settings.worker_poll_interval,
            )
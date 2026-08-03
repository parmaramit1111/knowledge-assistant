import asyncio
from app.core.logging import get_logger

from app.core.config import settings
from app.workers.base import BaseWorker
from app.workers.document.document_worker import DocumentWorker
from app.workers.document.chunk_worker import ChunkWorker
from app.workers.document.embedding_worker import EmbeddingWorker

logger = get_logger(__name__)


class Scheduler:
    """
    Simple polling scheduler for background workers.
    """

    def __init__(self) -> None:
        self.workers: list[BaseWorker] = [
            DocumentWorker(),
            ChunkWorker(),
            EmbeddingWorker(),
        ]

    async def start(self) -> None:
        logger.info(
            "Scheduler started with %d worker(s). Interval=%d seconds.",
            len(self.workers),
            settings.worker_interval_seconds,
        )

        try:
            while True:
                logger.debug(
                    "Executing %d worker(s)...",
                    len(self.workers),
                )

                for worker in self.workers:
                    try:
                        await worker.run()

                    except Exception:
                        logger.exception(
                            "%s failed",
                            worker.__class__.__name__,
                        )

                await asyncio.sleep(
                    settings.worker_interval_seconds,
                )

        except asyncio.CancelledError:
            logger.info("Scheduler stopped.")
            raise
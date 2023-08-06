from django.core.management.base import BaseCommand

from urlid_graph.utils import working
from urlid_graph.models import ObjectRepository


class Command(BaseCommand):
    help = "Update/create full-text search index"

    def add_arguments(self, parser):
        parser.add_argument(
            "--lock", action="store_true", default=False, help="Lock view for reading during refresh (faster)"
        )
        parser.add_argument(
            "--rebuild", action="store_true", default=False, help="Rebuild materialized view - needed when add new model or import new data"
        )

    def handle(self, *args, **kwargs):
        lock = kwargs["lock"]
        concurrently = not lock
        rebuild = kwargs["rebuild"]

        lock_text = "(with lock)" if lock else "(without lock)"
        with working(f"Refreshing object materialized view {lock_text}"):
            ObjectRepository.objects.refresh(concurrently=concurrently, rebuild=rebuild)

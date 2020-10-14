from django.core.management.base import BaseCommand, CommandError
from agencies.models import Source

class Command(BaseCommand):
    help = 'Initialise with preloaded news sources'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        sources = ["thestar", "malaysiakini", "freemalaysiatoday", "theborneopost"]

        for obj in sources:
            Source.objects.get_or_create(name=obj)
        self.stdout.write(self.style.SUCCESS('Success adding sources.') )

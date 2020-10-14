from django.core.management.base import BaseCommand, CommandError
from agencies.models import Source

class Command(BaseCommand):
    help = 'Initialise with preloaded news sources'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        sources = [
            {'name': 'thestar'          , 'rss': 'https://thestar.com.my/rss/News/Nation'},
            {'name': 'malaysiakini'     , 'rss': 'https://www.malaysiakini.com/rss/en/news.rss'},
            {'name': 'freemalaysiatoday', 'rss': 'https://www.freemalaysiatoday.com/rss'},
            {'name': 'theborneopost'    , 'rss': 'https://www.theborneopost.com/rss'},
            {'name': 'malaymail'        , 'rss': 'https://www.malaymail.com/feed/rss/malaysia'},
        ]

        for obj in sources:
            Source.objects.get_or_create(name=obj['name'], rss=obj['rss'])
        self.stdout.write(self.style.SUCCESS('Success adding sources.') )

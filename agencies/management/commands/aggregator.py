from django.core.management.base import BaseCommand, CommandError
from agencies.models import Agency, Source
from politicians.models import Politician

from bs4 import BeautifulSoup
import feedparser
import ssl
import requests
from dateutil import parser

class Command(BaseCommand):
    help = 'Initialise with preloaded news sources'

    def add_arguments(self, parser):
        parser.add_argument('--init', action='store_true', help='Initialise news sources.')
        parser.add_argument('--rss', action='store_true', help='Run aggregator.')

    def initialise(self):
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
    def rss(self):
        sources = Source.objects.all().values('id', 'name', 'rss')
        for source in sources:
            rss = source['rss']
            if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
            feed = feedparser.parse(rss)
            last_etag = feed.get('etag', '')
            last_modified = feed.get('modified', '')
            NewsFeed = feedparser.parse(rss, etag=last_etag, modified=last_modified)
            #self.stdout.write(self.style.SUCCESS(rss + ' ' + NewsFeed.get('status') + ' ' + NewsFeed.get('debug_message') + ' ' + NewsFeed.get('modified') ) )
            if NewsFeed.get('status') == 200:
                self.stdout.write(self.style.SUCCESS(rss + ' ' + str(NewsFeed.get('status') ) + ' ' + str(NewsFeed.get('modified') ) ) )
            else:
                self.stdout.write(self.style.WARNING(rss + ' ' + str(NewsFeed.get('status') ) ) )
                self.stdout.write(self.style.WARNING(str(NewsFeed.get('debug_message') ) ) )
        
            politicians = Politician.objects.filter().values('id', 'name')
            for politician in politicians:
                politician_name = politician['name'].replace('_', ' ')
                for entry in feed.entries:
                    #entry.title, description, published, link, guid
                    entry.published = parser.parse(str(entry.published) )
                    if source['name'] == "freemalaysiatoday" or source['name'] == "theborneopost" or source['name'] == "malaymail":
                        if politician_name in entry.title or politician_name in entry.description or politician_name in entry.content[0].value:
                            #check if already added
                            if source['name'] == "malaymail":
                                entry.guid = entry.guid.split("/")[-1]
                            else:
                                if "https://" in entry.guid:
                                    entry.guid = entry.guid.split("=")[1]
                            if Agency.objects.filter(headline=entry.title, politician=Politician.objects.get(id=politician['id']), source=Source.objects.get(id=source['id']), guid=entry.guid).count() > 0:
                                continue
                            agency = Agency.objects.create(headline=entry.title, source=Source.objects.get(id=source['id']), published=entry.published, link=entry.link, guid=entry.guid)
                            agency.save()
                            agency.politician.add(Politician.objects.get(id=politician['id']) )
                    else:
                        if politician_name in entry.title or politician_name in entry.description:
                            #check if already added
                            if Agency.objects.filter(headline=entry.title, politician=Politician.objects.get(id=politician['id']), source=Source.objects.get(id=source['id']), guid=entry.guid).count() > 0:
                                continue
                            agency = Agency.objects.create(headline=entry.title, source=Source.objects.get(id=source['id']), published=entry.published, link=entry.link, guid=entry.guid)
                            agency.save()
                            agency.politician.add(Politician.objects.get(id=politician['id']) )
    def handle(self, *args, **options):
        if options['init']:
            self.initialise()
        if options['rss']:
            self.rss()

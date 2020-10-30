from django.core.management.base import BaseCommand, CommandError
from agencies.models import Agency, Source
from politicians.models import Politician

from bs4 import BeautifulSoup
import feedparser
import ssl
import requests
from datetime import datetime
from dateutil import parser

class Command(BaseCommand):
    help = 'Initialise with preloaded news sources'

    def add_arguments(self, parser):
        parser.add_argument('--init', action='store_true', help='Initialise news sources.')
        parser.add_argument('--rss', action='store_true', help='Run aggregator.')
        parser.add_argument('--scrap', action='store_true', help='Run scrapper.')

    def initialise(self):
        sources = [
            {'name': 'thestar'          , 'rss': 'https://thestar.com.my/rss/News/Nation', 'type': 'agg'},
            {'name': 'malaysiakini'     , 'rss': 'https://www.malaysiakini.com/rss/en/news.rss', 'type': 'agg'},
            {'name': 'freemalaysiatoday', 'rss': 'https://www.freemalaysiatoday.com/rss', 'type': 'agg'},
            {'name': 'theborneopost'    , 'rss': 'https://www.theborneopost.com/rss', 'type': 'agg'},
            {'name': 'malaymail'        , 'rss': 'https://www.malaymail.com/feed/rss/malaysia', 'type': 'agg'},
            {'name': 'sebenarnya'       , 'rss': 'https://sebenarnya.my/rss', 'type': 'agg'},
            {'name': 'ukas_sarawak'     , 'rss': 'https://ukas.sarawak.gov.my/modules/web/pages/news/rss.php', 'type': 'agg'},
            {'name': 'sinarharian'      , 'rss': 'https://www.sinarharian.com.my/rssFeed/212/65', 'type': 'agg'},
            {'name': 'orientaldaily'    , 'rss': 'https://www.orientaldaily.com.my/feeds/rss/nation', 'type': 'agg'},
            {'name': 'seehua'           , 'rss': 'http://news.seehua.com/?cat=3', 'type': 'scrap'},
            {'name': 'sinchew_sarawak'  , 'rss': 'https://sarawak.sinchew.com.my/', 'type': 'scrap'},
        ]
        for obj in sources:
            if Source.objects.filter(name=obj['name']).count():
                continue
            else:
                Source.objects.create(name=obj['name'], rss=obj['rss'], type=obj['type'])
        self.stdout.write(self.style.SUCCESS('Success adding sources.') )
    def scrap(self):
        sources = Source.objects.filter(type="scrap").values('id', 'name', 'rss', 'type')
        for source in sources:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get(source['rss'], headers=headers)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(source['rss'] + ' ' + str(response.status_code) ) )
            else:
                self.stdout.write(self.style.WARNING(source['rss']+ ' ' + str(response.status_code) ) )
            soup = BeautifulSoup(response.text, features="html.parser")

            if source['name'] == 'seehua':
                entries = soup.find_all('div', {'class': 'td-block-span6'})

                politicians = Politician.objects.filter().values('id', 'name', 'othername')
                for politician in politicians:
                    politician_name = politician['othername']
                    if politician_name == "":
                        continue
                    for entry in entries:
                        link = entry.find('a');
                        sec_response = requests.get(link['href'], headers=headers)
                        sec_soup = BeautifulSoup(sec_response.text, features="html.parser")
                        #look into the news item
                        description = sec_soup.find('div', {'class': 'td-post-content'}).getText()
                        title = link['title']
                        published = parser.parse(str(entry.find('time')['datetime']) )
                        guid = link['href'].split("=")[1]
                        featuredtag = sec_soup.find('div',{'class': 'td-post-featured-image'})
                        first_image_url = ""
                        if featuredtag:
                            first_image_url = featuredtag.find('img')['src']
                        #record into the database
                        if politician_name in title or politician_name in description:
                            #check if already added
                            if Agency.objects.filter(headline=title, politician=Politician.objects.get(id=politician['id']), source=Source.objects.get(name=source['name']), guid=guid).count():
                                agency = Agency.objects.filter(headline=title).update(headline=title, source=Source.objects.get(name=source['name']), published=published, link=link['href'], first_image_url=first_image_url, guid=guid)
                            else:
                                agency = Agency.objects.create(headline=title, source=Source.objects.get(name=source['name']), published=published, link=link['href'], first_image_url=first_image_url, guid=guid)
                                agency.save()
                                agency.politician.add(Politician.objects.get(id=politician['id']) )
                
    def rss(self):
        sources = Source.objects.filter(type="agg").values('id', 'name', 'rss', 'type')
        for source in sources:
            if source == "ukas_sarawak": continue
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
                    if source['name'] == "ukas_sarawak":
                        try:
                            d = datetime.strptime(str(entry.published), "%Y %b %d %z")
                            entry.published = d.strftime("%Y-%m-%d %H:%M:%S%z")
                        except ValueError:
                            entry.published = parser.parse(str(entry.published) )
                    else:
                        entry.published = parser.parse(str(entry.published) )
                    if source['name'] == "freemalaysiatoday" or source['name'] == "theborneopost" or source['name'] == "malaymail":
                        #RSS contains content tag
                        if politician_name in entry.title or politician_name in entry.description or politician_name in entry.content[0].value:
                            #check if already added
                            if source['name'] == "malaymail":
                                entry.guid = entry.guid.split("/")[-1]
                            else:
                                if "https://" in entry.guid:
                                    entry.guid = entry.guid.split("=")[1]
                            if Agency.objects.filter(headline=entry.title, politician=Politician.objects.get(id=politician['id']), source=Source.objects.get(id=source['id']), guid=entry.guid).count() > 0:
                                continue
                            #get first image url
                            first_image_url = ""
                            soup = BeautifulSoup(entry.content[0].value, features="html.parser")
                            if soup.find('img'):
                                first_image_url = soup.find('img')['src']

                            agency = Agency.objects.create(headline=entry.title, source=Source.objects.get(id=source['id']), published=entry.published, link=entry.link, first_image_url=first_image_url, guid=entry.guid)
                            agency.save()
                            agency.politician.add(Politician.objects.get(id=politician['id']) )
                    else:
                        #RSS does not contain content tag
                        if politician_name in entry.title or politician_name in entry.description:
                            if source['name'] == "sebenarnya":
                                if "https://" in entry.guid:
                                    entry.guid = entry.guid.split("=")[1]
                            elif source['name'] == "ukas_sarawak":
                                if "https://" in entry.link:
                                    entry.guid = entry.link.split("=")[-1]
                            elif source['name'] == "sinarharian":
                                if "https://" in entry.link:
                                    entry.guid = entry.link.split("/")[4]
                            #check if already added
                            if Agency.objects.filter(headline=entry.title, politician=Politician.objects.get(id=politician['id']), source=Source.objects.get(id=source['id']), guid=entry.guid).count() > 0:
                                continue
                            first_image_url = "" 
                            if source['name'] == "ukas_sarawak":
                                #get first image url
                                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                                response = requests.get(entry.link, headers=headers)
                                soup = BeautifulSoup(response.text, features="html.parser")
                                news_data = soup.find('td', {'class': 'news_data'})
                                first_image_url = "https://ukas.sarawak.gov.my" + news_data.find('img')['src']
                            elif source['name'] == "sinarharian":
                                first_image_url = entry.href
                            #print(entry.title, entry.published, entry.link, first_image_url, entry.guid)
                            agency = Agency.objects.create(headline=entry.title, source=Source.objects.get(id=source['id']), published=entry.published, link=entry.link, first_image_url=first_image_url, guid=entry.guid)
                            agency.save()
                            agency.politician.add(Politician.objects.get(id=politician['id']) )
    def handle(self, *args, **options):
        if options['init']:
            self.initialise()
        if options['rss']:
            self.rss()
        if options['scrap']:
            self.scrap()

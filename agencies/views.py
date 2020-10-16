from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from dateutil import parser

from politicians.models import Politician
from agencies.models import Agency, Source

from bs4 import BeautifulSoup
import feedparser
import ssl
import requests

@user_passes_test(lambda u: u.is_superuser)
def scrap(request):
    origins = {"sinchew": "https://www.sinchew.com.my/column/node_7075.html"}
    for origin in origins:
        results = {}
        url = origins[origin]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        articles = soup.find('div', {'id' : 'articlenum'})
        listings = articles.find_all('li', {'class' : 'listing'})

        source = Source.objects.filter(name=origin)
        politicians = Politician.objects.filter().values('id', 'othername')
        for politician in politicians:
            for listing in listings:
                titlediv = listing.find_all('div')[1]
                obj = titlediv.find('a')
                #TODO: Handle case when there is no div on element[0] which is an image div
                if obj is None:
                    continue
                title = obj.get_text()
                link = obj['href']
                description = listing.find_all('div')[3].get_text()
                time = listing.find('div', {'id' : 'time'}).get_text()
                article_id = link.split('_')[1][:-5]
    
                #print(title, link, description, time, article_id)
                time = parser.parse(time)
                if politician['othername'] != "" and (politician['othername'] in title or politician['othername'] in description):
                    if Agency.objects.filter(politician=Politician.objects.get(othername=politician['othername']), source=Source.objects.get(name=origin), guid=article_id).count() > 0:
                        continue
                    agency = Agency.objects.create(headline=title, source=Source.objects.get(name=origin), published=time, link=link, guid=article_id)
                    agency.save()
                    agency.politician.add(Politician.objects.get(id=politician['id']) )
                #TODO: parse for politician name in the next content page
                results[article_id] = link
        
    return render(request, 'agencies/scrap.html', {"results" : results })
        
@user_passes_test(lambda u: u.is_superuser)
def aggregator(request):
    statuses = []
    sources = Source.objects.all().values('id', 'name', 'rss')
    for source in sources:
        rss = source['rss']
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        feed = feedparser.parse(rss)
        last_etag = feed.get('etag', '')
        last_modified = feed.get('modified', '')
        NewsFeed = feedparser.parse(rss, etag=last_etag, modified=last_modified)
        statuses.append( {'source': rss, 'status': NewsFeed.get('status'), 'debug': NewsFeed.get('debug_message'), 'modified': NewsFeed.get('modified') } )
    
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
                        first_image_url = ""
                        soup = BeautifulSoup(entry.content[0].value, features="html.parser")
                        if soup.find('img'):
                            first_image_url = soup.find('img')['src']
                        agency = Agency.objects.create(headline=entry.title, source=Source.objects.get(id=source['id']), published=entry.published, link=entry.link, first_image_url=first_image_url, guid=entry.guid)
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
    return render(request, 'agencies/aggregator.html', {'statuses': statuses} )

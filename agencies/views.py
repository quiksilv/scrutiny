from django.shortcuts import render

from politicians.models import Politician
from agencies.models import Agency, Source
import feedparser
import ssl

# Create your views here.
def aggregator(request):
    statuses = []
    sources = ["thestar", "malaysiakini", "freemalaysiatoday", "theborneopost"]
    for source_name in sources:
        if source_name == "thestar":
            url = "https://thestar.com.my/rss/News/Nation"
            #url = "thestar.rss"
        if source_name == "malaysiakini":
            url = "https://www.malaysiakini.com/rss/en/news.rss"
        if source_name == "freemalaysiatoday":
            url = "https://www.freemalaysiatoday.com/rss"
        if source_name == "theborneopost":
            url = "https://www.theborneopost.com/rss"
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        feed = feedparser.parse(url)
        last_etag = feed.get('etag', '')
        last_modified = feed.get('modified', '')
        NewsFeed = feedparser.parse(url, etag=last_etag, modified=last_modified)
        statuses.append( {'source': source_name, 'status': NewsFeed.get('status'), 'debug': NewsFeed.get('debug_message'), 'modified': NewsFeed.get('modified') } )
    
        source = Source.objects.filter(name=source_name)
        politicians = Politician.objects.filter().values('id', 'name')
        for politician in politicians:
            for entry in feed.entries:
                #entry.title, description, published, link, guid
                if source_name == "freemalaysiatoday" or source_name == "theborneopost":
                    if politician['name'] in entry.title or politician['name'] in entry.description or politician['name'] in entry.content[0].value:
                        #check if already added
                        entry.guid = entry.guid.split("=")[1]
                        if Agency.objects.filter(source=Source.objects.get(name=source_name), guid=entry.guid).count() > 0:
                            continue
                        agency = Agency.objects.create(headline=entry.title, source=Source.objects.get(name=source_name), published=entry.published, link=entry.link, guid=entry.guid)
                        agency.save()
                        agency.politician.add(Politician.objects.get(id=politician['id']) )
                else:
                    if politician['name'] in entry.title or politician['name'] in entry.description:
                        #check if already added
                        if Agency.objects.filter(source=Source.objects.get(name=source_name), guid=entry.guid).count() > 0:
                            continue
                        agency = Agency.objects.create(headline=entry.title, source=Source.objects.get(name=source_name), published=entry.published, link=entry.link, guid=entry.guid)
                        agency.save()
                        agency.politician.add(Politician.objects.get(id=politician['id']) )
    return render(request, 'agencies/aggregator.html', {'statuses': statuses} )
                    

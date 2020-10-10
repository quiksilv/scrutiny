from django.shortcuts import render

from politicians.models import Politician
from agencies.models import Agency, Source
import feedparser
import ssl

# Create your views here.
def thestar(request):
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
        #NewsFeed = feedparser.parse("https://thestar.com.my/rss/News/Nation")
        NewsFeed = feedparser.parse("sample.rss")

        source = Source.objects.filter(name="thestar")
        politicians = Politician.objects.filter().values('id', 'name')
        for politician in politicians:
            for entry in NewsFeed.entries:
                #print (entry.title)
                #print (entry.description)
                #print (entry.published)
                if politician['name'] in entry.title or politician['name'] in entry.description:
                    agency = Agency.objects.create(headline=entry.title, source=Source.objects.get(name="thestar") )
                    agency.save()
                    agency.politician.add(Politician.objects.get(id=politician['id']) )

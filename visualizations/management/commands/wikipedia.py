from django.core.management.base import BaseCommand, CommandError
from politicians.models import Politician
from visualizations.models import Statistics
import requests, os, json, datetime
from dateutil import parser

class Command(BaseCommand):
    help = 'Get daily tweet statistics'
    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Obtain all wikipedia user statistics.')
    def connect_to_endpoint(self, url, headers):
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return json.loads(response.text)
    def handle(self, *args, **options):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
        if options['all']:
            politicians = Politician.objects.all().values('wikipedia')
            for politician in politicians:
                if not politician['wikipedia']:
                    continue
                url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + politician['wikipedia']
                yesterday = datetime.date.today() + datetime.timedelta(days=-2)
                yesterday = yesterday.strftime("%Y%m%d")
                today = datetime.date.today() + datetime.timedelta(days=-1)
                today = today.strftime("%Y%m%d")
                url2 = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/" + politician['wikipedia'] + "/daily/" + yesterday + "12/" + today + "12"
                metrics = {}
                metrics['timestamp'] = parser.parse(str(self.connect_to_endpoint(url, headers)['timestamp']) ).timestamp()
                metrics['daily_pageview'] = self.connect_to_endpoint(url2, headers)['items'][0]['views']
                Statistics.objects.create(category='wikipedia', name='timestamp', value=metrics['timestamp'], politician=Politician.objects.get(wikipedia=politician['wikipedia']) )
                Statistics.objects.create(category='wikipedia', name='daily_pageview', value=metrics['daily_pageview'], politician=Politician.objects.get(wikipedia=politician['wikipedia']) )
                self.stdout.write(self.style.SUCCESS(politician['wikipedia'] + " recorded.") )

from django.core.management.base import BaseCommand, CommandError
from politicians.models import Politician
from visualizations.models import Statistics
import requests, os, json

class Command(BaseCommand):
    help = 'Get daily tweet statistics'
    def add_arguments(self, parser):
        parser.add_argument('--test', type=str, help='Obtain test data. Only one twitter user statistics.')
        parser.add_argument('--all', action='store_true', help='Obtain all twitter user statistics.')
    def connect_to_endpoint(self, url, headers):
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return json.loads(response.text)
    def handle(self, *args, **options):
        bearer_token = os.environ['TWITTER_API_V2_BEARER_TOKEN']
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        if options['test']:
            username = options['test']
            politician = Politician.objects.get(twitter=username)
            if not politician:
                self.stdout.write(self.style.WARNING('Twitter handle does not exist in the politicians table.') )
                return
            url = "https://api.twitter.com/2/users/by/username/" + username + "?user.fields=public_metrics"
            metrics = self.connect_to_endpoint(url, headers)['data']['public_metrics']
            for key, value in metrics.items():
                Statistics.objects.create(category='tweets', name=key, value=value, politician=Politician.objects.get(twitter=username) )
        if options['all']:
            politicians = Politician.objects.all().values('twitter')
            for politician in politicians:
                if not politician['twitter']:
                    continue
                url = "https://api.twitter.com/2/users/by/username/" + politician['twitter'] + "?user.fields=public_metrics"
                metrics = self.connect_to_endpoint(url, headers)['data']['public_metrics']
                for key, value in metrics.items():
                    Statistics.objects.create(category='tweets', name=key, value=value, politician=Politician.objects.get(twitter=politician['twitter']) )
                self.stdout.write(self.style.SUCCESS(politician['twitter'] + " recorded.") )

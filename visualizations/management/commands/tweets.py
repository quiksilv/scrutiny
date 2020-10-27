from django.core.management.base import BaseCommand, CommandError
from politicians.models import Politician
from visualizations.models import Statistics
import requests, os, json, datetime

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
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Authorization": "Bearer {}".format(bearer_token)}
        if options['test']:
            username = options['test']
            politician = Politician.objects.get(twitter=username)
            if not politician:
                self.stdout.write(self.style.WARNING('Twitter handle does not exist in the politicians table.') )
                return
            #user fields
            url = "https://api.twitter.com/2/users/by/username/" + username + "?user.fields=public_metrics"
            data = self.connect_to_endpoint(url, headers)['data']
            metrics = data['public_metrics']
            yesterday = datetime.date.today() + datetime.timedelta(days=-2)
            yesterday = yesterday.strftime("%Y-%m-%dT00:00:00Z")
            #user tweet fields
            url = "https://api.twitter.com/2/tweets/search/recent?query=from:" + username + "&tweet.fields=public_metrics&start_time=" + yesterday
            data = self.connect_to_endpoint(url, headers)
            metrics['total_like_count'] = 0
            metrics['total_quote_count'] = 0
            metrics['total_reply_count'] = 0
            metrics['total_retweet_count'] = 0
            if not 'data' in data:
                self.stdout.write(self.style.WARNING(username + " has no tweets for the past day.") )
                return
            else:
                for d in data['data']:
                    metrics['total_like_count'] += d['public_metrics']['like_count']
                    metrics['total_quote_count'] += d['public_metrics']['quote_count']
                    metrics['total_reply_count'] += d['public_metrics']['reply_count']
                    metrics['total_retweet_count'] += d['public_metrics']['retweet_count']
                metrics['total_tweets'] = data['meta']['result_count']
            for key, value in metrics.items():
                Statistics.objects.create(category='tweets', name=key, value=value, politician=Politician.objects.get(twitter=username) )
            self.stdout.write(self.style.SUCCESS(username + " recorded.") )
        if options['all']:
            politicians = Politician.objects.all().values('twitter')
            for politician in politicians:
                if not politician['twitter']:
                    continue
                #user fields
                url = "https://api.twitter.com/2/users/by/username/" + politician['twitter'] + "?user.fields=public_metrics"
                data = self.connect_to_endpoint(url, headers)['data']
                metrics = data['public_metrics']
                yesterday = datetime.date.today() + datetime.timedelta(days=-2)
                yesterday = yesterday.strftime("%Y-%m-%dT00:00:00Z")
                #user tweet fields
                url = "https://api.twitter.com/2/tweets/search/recent?query=from:" + politician['twitter'] + "&tweet.fields=public_metrics&start_time=" + yesterday
                data = self.connect_to_endpoint(url, headers)
                metrics['total_like_count'] = 0
                metrics['total_quote_count'] = 0
                metrics['total_reply_count'] = 0
                metrics['total_retweet_count'] = 0
                #if no tweets
                if not 'data' in data:
                    self.stdout.write(self.style.WARNING(politician['twitter'] + " has no tweets for the past day.") )
                    continue
                for d in data['data']:
                    metrics['total_like_count'] += d['public_metrics']['like_count']
                    metrics['total_quote_count'] += d['public_metrics']['quote_count']
                    metrics['total_reply_count'] += d['public_metrics']['reply_count']
                    metrics['total_retweet_count'] += d['public_metrics']['retweet_count']
                metrics['total_tweets'] = data['meta']['result_count']
                for key, value in metrics.items():
                    Statistics.objects.create(category='tweets', name=key, value=value, politician=Politician.objects.get(twitter=politician['twitter']) )
                self.stdout.write(self.style.SUCCESS(politician['twitter'] + " recorded.") )

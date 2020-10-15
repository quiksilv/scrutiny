from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import requests

class Command(BaseCommand):
    help = 'Initialise with preloaded data'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        url = "https://duns.sarawak.gov.my/page-0-40-150-Maklumat-Ahli-DUN-Sarawak.html"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        img_srcs = soup.find_all('img')
        for img_src in img_srcs:
            if img_src.parent.name == 'a' and img_src.parent.get('title'):
                #print(img_src.parent.get('title'), img_src.get('src'))
                print(img_src.get('src'))

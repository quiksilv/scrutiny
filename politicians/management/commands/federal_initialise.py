from django.core.management.base import BaseCommand, CommandError
from politicians.models import Party, Constituency, Portfolio, Politician

class Command(BaseCommand):
    help = 'Initialise with preloaded data'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        parties = [
            {'abbr': 'IND', 'english_name': 'Independent', 'malay_name': '', 'chinese_name': '', 'iban_name': '', 'tamil_name': ''},
            {'abbr': 'DAP', 'english_name': 'Democratic Action Party', 'malay_name': 'Parti Tindakan Demokratik', 'chinese_name': '民主行動黨', 'iban_name': '', 'tamil_name': 'ஜனநாயக செயல் கட்சி'},
            {'abbr': 'PKR', 'english_name': 'People\'s Justice Party', 'malay_name': 'Parti Keadilan Rakyat', 'chinese_name': '人民公正黨', 'iban_name': '', 'tamil_name': 'மக்கள் நீதி கட்சி'},
            {'abbr': 'BERSATU', 'english_name': 'Malaysian United Indigenous Party', 'malay_name': 'Parti Pribumi Bersatu Malaysia', 'chinese_name': '马来西亚土著团结党', 'iban_name': '', 'tamil_name': 'பிபிபீஏம் (மலேசிய ஐக்கிய மக்கள் கட்சி)'},
        ]
        for party in parties:
            Party.objects.get_or_create(abbr=party['abbr'], english_name=party['english_name'], malay_name=party['malay_name'], chinese_name=party['chinese_name'], iban_name=party['iban_name'])
        self.stdout.write(self.style.SUCCESS('Success adding parties.') )
        federal = [
            {'code': 'P.132',  'name': 'Port Dickson'},
        ]
        for obj in federal:
            Constituency.objects.get_or_create(state='Federal', code=obj['code'], name=obj['name'])
        self.stdout.write(self.style.SUCCESS('Success adding constituencies.') )

        portfolios = [
            {'name': 'Opposition Leader', 'othername': ''},
        ]
        for obj in portfolios:
            Portfolio.objects.get_or_create(name=obj['name'])
        self.stdout.write(self.style.SUCCESS('Success adding portfolios.') )
        politicians = [
            {'image_url': 'https://www.parlimen.gov.my/images/webuser/ahli/2018/YB%20Port%20Dickson.png', 'party': 'PKR', 'name':'Anwar Ibrahim'                , 'firstname':'Anwar'    , 'lastname':'Ibrahim', 'othername':'', 'constituency':'Port Dickson', 'portfolio':['Opposition Leader']},
        ]
        for obj in politicians:
            party = Party.objects.get(abbr=obj['party'])
            politician, created = Politician.objects.get_or_create(image_url=obj['image_url'], party=party, name=obj['name'], firstname=obj['firstname'], lastname=obj['lastname'], othername=obj['othername'])
            Constituency.objects.filter(name=obj['constituency']).update(politician=politician)
            if obj['portfolio'] != '':
                for portfolio in obj['portfolio']:
                    Portfolio.objects.filter(name=portfolio).update(politician=politician)
        self.stdout.write(self.style.SUCCESS('Success adding politicians.') )

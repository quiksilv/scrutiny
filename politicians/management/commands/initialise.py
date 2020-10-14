from django.core.management.base import BaseCommand, CommandError
from politicians.models import Constituency, Portfolio, Politician

class Command(BaseCommand):
    help = 'Initialise with preloaded data'

    def add_arguments(self, parser):
        return

    def handle(self, *args, **options):
        sarawak = [
            {'code': 'N.1',  'name': 'Opar'},
            {'code': 'N.2',  'name': 'Tasik Biru'},
            {'code': 'N.3',  'name': 'Tanjung Datu'},
            {'code': 'N.4',  'name': 'Pantai Damai'},
            {'code': 'N.5',  'name': 'Demak Laut'},
            {'code': 'N.6',  'name': 'Tupong'},
            {'code': 'N.7',  'name': 'Samariang'},
            {'code': 'N.8',  'name': 'Satok'},
            {'code': 'N.9',  'name': 'Padungan'},
            {'code': 'N.10', 'name': 'Pending'},
            {'code': 'N.11', 'name': 'Batu Lintang'},
            {'code': 'N.12', 'name': 'Kota Sentosa'},
            {'code': 'N.13', 'name': 'Batu Kitang'},
            {'code': 'N.14', 'name': 'Batu Kawah'},
            {'code': 'N.15', 'name': 'Asajaya'},
            {'code': 'N.16', 'name': 'Muara Tuang'},
            {'code': 'N.17', 'name': 'Stakan'},
            {'code': 'N.18', 'name': 'Serembu'},
            {'code': 'N.19', 'name': 'Mambong'},
            {'code': 'N.20', 'name': 'Tarat'},
            {'code': 'N.21', 'name': 'Tebedu'},
            {'code': 'N.22', 'name': 'Kedup'},
            {'code': 'N.23', 'name': 'Bukit Semuja'},
            {'code': 'N.24', 'name': 'Sadong Jaya'},
            {'code': 'N.25', 'name': 'Simunjan'},
            {'code': 'N.26', 'name': 'Gedong'},
            {'code': 'N.27', 'name': 'Sebuyau'},
            {'code': 'N.28', 'name': 'Lingga'},
            {'code': 'N.29', 'name': 'Beting Maro'},
            {'code': 'N.30', 'name': 'Balai Ringin'},
            {'code': 'N.31', 'name': 'Bukit Begunan'},
            {'code': 'N.32', 'name': 'Simanggang'},
            {'code': 'N.33', 'name': 'Engkilili'},
            {'code': 'N.34', 'name': 'Batang Ai'},
            {'code': 'N.35', 'name': 'Saribas'},
            {'code': 'N.36', 'name': 'Layar'},
            {'code': 'N.37', 'name': 'Bukit Saban'},
            {'code': 'N.38', 'name': 'Kalaka'},
            {'code': 'N.39', 'name': 'Krian'},
            {'code': 'N.40', 'name': 'Kabong'},
            {'code': 'N.41', 'name': 'Kuala Rajang'},
            {'code': 'N.42', 'name': 'Semop'},
            {'code': 'N.43', 'name': 'Daro'},
            {'code': 'N.44', 'name': 'Jemoreng'},
            {'code': 'N.45', 'name': 'Repok'},
            {'code': 'N.46', 'name': 'Meradong'},
            {'code': 'N.47', 'name': 'Pakan'},
            {'code': 'N.48', 'name': 'Meluan'},
            {'code': 'N.49', 'name': 'Ngemah'},
            {'code': 'N.50', 'name': 'Machan'},
            {'code': 'N.51', 'name': 'Bukit Assek'},
            {'code': 'N.52', 'name': 'Dudong'},
            {'code': 'N.53', 'name': 'Bawang Assan'},
            {'code': 'N.54', 'name': 'Pelawan'},
            {'code': 'N.55', 'name': 'Nangka'},
            {'code': 'N.56', 'name': 'Dalat'},
            {'code': 'N.57', 'name': 'Tellian'},
            {'code': 'N.58', 'name': 'Balingian'},
            {'code': 'N.59', 'name': 'Tamin'},
            {'code': 'N.60', 'name': 'Kakus'},
            {'code': 'N.61', 'name': 'Pelagus'},
            {'code': 'N.62', 'name': 'Katibas'},
            {'code': 'N.63', 'name': 'Bukit Goram'},
            {'code': 'N.64', 'name': 'Baleh'},
            {'code': 'N.65', 'name': 'Belaga'},
            {'code': 'N.66', 'name': 'Murum'},
            {'code': 'N.67', 'name': 'Jepak'},
            {'code': 'N.68', 'name': 'Tanjong Batu'},
            {'code': 'N.69', 'name': 'Kemena'},
            {'code': 'N.70', 'name': 'Samalaju'},
            {'code': 'N.71', 'name': 'Bekenu'},
            {'code': 'N.72', 'name': 'Lambir'},
            {'code': 'N.73', 'name': 'Piasau'},
            {'code': 'N.74', 'name': 'Pujut'},
            {'code': 'N.75', 'name': 'Senadin'},
            {'code': 'N.76', 'name': 'Marudi'},
            {'code': 'N.77', 'name': 'Telang Usan'},
            {'code': 'N.78', 'name': 'Mulu'},
            {'code': 'N.79', 'name': 'Bukit Kota'},
            {'code': 'N.80', 'name': 'Batu Danau'},
            {'code': 'N.81', 'name': 'Ba\'kelalan'},
            {'code': 'N.82', 'name': 'Bukit Sari'},
        ]
        for obj in sarawak:
            Constituency.objects.get_or_create(state='sarawak', code=obj['code'], name=obj['name'])
        self.stdout.write(self.style.SUCCESS('Success adding constituencies.') )

        portfolios = [
            {'name': 'Chief Minister', 'othername': ''},
            {'name': 'Minister of Finance and Economic Planning', 'othername': ''},
            {'name': 'Minister of Urban Development and Resources', 'othername': ''},
            {'name': 'Deputy Chief Minister', 'othername': ''},
            {'name': 'Minister of Agriculture, Native Land and Regional Development', 'othername': ''},
            {'name': 'Second Minister of Finance', 'othername': ''},
            {'name': 'Minister of Infrastructural and Ports Development', 'othername': ''},
            {'name': 'Minister of International Trade and Industry, Industrial Terminal and Entrepreneur Development', 'othername': ''},
            {'name': 'Second Minister of Urban Development and Resources ', 'othername': ''},
            {'name': 'Minister in the Chief Minister\'s Office', 'othername': ''},
            {'name': 'Minister of Education, Science and Technological Research', 'othername': ''},
            {'name': 'Minister of Local Government and Housing', 'othername': ''},
            {'name': 'Minister of Tourism, Art, Culture', 'othername': ''},
            {'name': 'Minister of Tourism, Art, Culture', 'othername': ''},
            {'name': 'Minister of Youth and Sports', 'othername': ''},
            {'name': 'Minister of Transport', 'othername': ''},
            {'name': 'Minister of Utilities', 'othername': ''},
            {'name': 'Minister of Welfare, Community Well-being, Women, Family and Childhood Development', 'othername': ''},
            {'name': 'Speaker', 'othername': ''},
            {'name': 'Deputy Speaker', 'othername': ''},
            {'name': 'Opposition Leader', 'othername': ''},
        ]
        for obj in portfolios:
            Portfolio.objects.get_or_create(name=obj['name'])
        self.stdout.write(self.style.SUCCESS('Success adding portfolios.') )

        politicians = [
            {'name':'Ranum_Mina'                            , 'firstname':'Ranum'           , 'lastname':'Mina'         , 'othername':'', 'constituency':'Opar'         , 'portfolio':''},
            {'name':'Henry_Harry_Jinep'                     , 'firstname':'Henry Harry'     , 'lastname':'Jinep'        , 'othername':'', 'constituency':'Tasik Biru'   , 'portfolio':''},
            {'name':'Jamilah_Anu'                           , 'firstname':'Jamilah'         , 'lastname':'Anu'          , 'othername':'', 'constituency':'Tanjung Datu' , 'portfolio':''},
            {'name':'Abdul_Rahman_Junaidi'                  , 'firstname':'Abdul Rahman'    , 'lastname':'Junaidi'      , 'othername':'', 'constituency':'Pantai Damai' , 'portfolio':''},
            {'name':'Hazland_Abang_Hipni'                   , 'firstname':'Hazland'         , 'lastname':'Abang Hipni'  , 'othername':'', 'constituency':'Demak Laut'   , 'portfolio':''},
            {'name':'Fazzrudin_Abdul_Rahman'                , 'firstname':'Fazzrudin'       , 'lastname':'Abdul Rahman' , 'othername':'', 'constituency':'Tupong'       , 'portfolio':''},
            {'name':'Sharifah_Hasidah_Sayeed_Aman_Ghazali'  , 'firstname':'Sharifah Hasidah', 'lastname':'Sayeed Aman Ghazali', 'othername':'', 'constituency':'Samariang', 'portfolio':''},
            {'name':'Abang_Abdul_Rahman_Zohari_Abang_Openg'  , 'firstname':'Abang_Abdul Rahman Zohari', 'lastname':'Abang Openg', 'othername':'', 'constituency':'Satok', 'portfolio':['Chief Minister', 'Minister of Finance and Economic Planning', 'Minister of Urban Development and Resources']},
            {'name':'Wong_King_Wei'                         , 'firstname':'King Wei'        , 'lastname':'Wong', 'othername':'', 'constituency':'Padungan', 'portfolio':''},
            {'name':'Violet_Yong_Wui_Wui'                   , 'firstname':'Wui Wui'         , 'lastname':'Yong', 'othername':'Violet Yong', 'constituency':'Pending', 'portfolio':''},
            {'name':'See_Chee_How'                          , 'firstname':'Chee How'        , 'lastname':'See', 'othername':'', 'constituency':'Batu Lintang', 'portfolio':''},
            {'name':'Chong_Chieng_Jen'                      , 'firstname':'Chieng Jen'      , 'lastname':'Chong', 'othername':'', 'constituency':'Kota Sentosa', 'portfolio':['Opposition Leader']},
            {'name':'Lo_Khere_Chiang'                       , 'firstname':'Khere Chiang'    , 'lastname':'Lo', 'othername':'', 'constituency':'Batu Kitang', 'portfolio':''},
            {'name':'Sim_Kui_Hian'                          , 'firstname':'Kui Hian'        , 'lastname':'Sim', 'othername':'', 'constituency':'Batu Kawah', 'portfolio':['Minister of Local Government and Housing']},
            {'name':'Abdul_Karim_Rahman_Hamzah'             , 'firstname':'Abdul Karim'     , 'lastname':'Rahman Hamzah', 'othername':'', 'constituency':'Asajaya', 'portfolio':['Minister of Tourism, Art, Culture', 'Minister of Youth and Sports']},
            {'name':'Idris_Buang'                           , 'firstname':'Idris'           , 'lastname':'Buang', 'othername':'', 'constituency':'Muara Tuang', 'portfolio':''},
            {'name':'Mohammad_Ali_Mahmud'                   , 'firstname':'Mohammad Ali'    , 'lastname':'Mahmud', 'othername':'', 'constituency':'Stakan', 'portfolio':''},
            {'name':'Miro_Simuh'                            , 'firstname':'Miro'            , 'lastname':'Simuh', 'othername':'', 'constituency':'Serembu', 'portfolio':''},
            {'name':'Jerip_Susil'                           , 'firstname':'Jerip'           , 'lastname':'Susil', 'othername':'', 'constituency':'Mambong', 'portfolio':''},
            {'name':'Roland_Sagah_Wee_Inn'                  , 'firstname':'Roland Sagah'    , 'lastname':'Wee Inn', 'othername':'', 'constituency':'Tarat', 'portfolio':''},
            {'name':'Michael_Manyin_Jawong'                 , 'firstname':'Micheal Manyin'  , 'lastname':'Jawong', 'othername':'', 'constituency':'Tebedu', 'portfolio':['Minister of Education, Science and Technological Research']},
            {'name':'Maclaine_Ben'                          , 'firstname':'Maclaine'        , 'lastname':'Ben', 'othername':'', 'constituency':'Kedup', 'portfolio':''},
            {'name':'John_Ilus'                             , 'firstname':'John'            , 'lastname':'Ilus', 'othername':'', 'constituency':'Bukit Semuja', 'portfolio':''},
            {'name':'Aidel_Lariwoo'                         , 'firstname':'Aidel'           , 'lastname':'Lariwoo', 'othername':'', 'constituency':'Sadong Jaya', 'portfolio':''},
            {'name':'Awla_Dris'                             , 'firstname':'Awla'            , 'lastname':'Dris', 'othername':'', 'constituency':'Simunjan', 'portfolio':''},
            {'name':'Mohd_Naroden_Majais'                   , 'firstname':'Mohd Naroden'    , 'lastname':'Majais', 'othername':'', 'constituency':'Gedong', 'portfolio':''},
            {'name':'Julaihi_Narawi'                        , 'firstname':'Julaihi'         , 'lastname':'Narawi', 'othername':'', 'constituency':'Sebuyau', 'portfolio':''},
            {'name':'Simoi_Peri'                            , 'firstname':'Simoi'           , 'lastname':'Peri', 'othername':'', 'constituency':'Lingga', 'portfolio':''},
            {'name':'Razaili_Gapor'                         , 'firstname':'Razaili'         , 'lastname':'Gapor', 'othername':'', 'constituency':'Beting Maro', 'portfolio':''},
            {'name':'Snowdan_Lawan'                         , 'firstname':'Snowdan'         , 'lastname':'Lawan', 'othername':'', 'constituency':'Balai Ringin', 'portfolio':''},
            {'name':'Mong_Dagang'                           , 'firstname':'Mong'            , 'lastname':'Dagang', 'othername':'', 'constituency':'Bukit Begunan', 'portfolio':''},
            {'name':'Francis_Harden_Hollis'                 , 'firstname':'Francis Harden'  , 'lastname':'Hollis', 'othername':'', 'constituency':'Simanggang', 'portfolio':''},
            {'name':'Johnichal_Rayong_Ngipa'                , 'firstname':'Johnical'        , 'lastname':'Ngipa', 'othername':'', 'constituency':'Engkilili', 'portfolio':''},
            {'name':'Malcom_Mussen_Lamoh'                   , 'firstname':'Malcom Mussen'   , 'lastname':'Lamoh', 'othername':'', 'constituency':'Batang Ai', 'portfolio':''},
            {'name':'Mohammad_Razi_Sitam'                   , 'firstname':'Mohammad Razi'   , 'lastname':'Sitam', 'othername':'', 'constituency':'Saribas', 'portfolio':''},
            {'name':'Gerald_Rentap_Jabu'                    , 'firstname':'Gerald Rentap'   , 'lastname':'Jabu', 'othername':'', 'constituency':'Layar', 'portfolio':''},
            {'name':'Douglas_Uggah_Embas'                   , 'firstname':'Douglas Uggah'   , 'lastname':'Embas', 'othername':'', 'constituency':'Bukit Saban', 'portfolio':['Deputy Chief Minister', 'Minister of Agriculture, Native Land and Regional Development', 'Second Minister of Finance']},
            {'name':'Abdul_Wahab_Aziz'                      , 'firstname':'Abdul Wahab'     , 'lastname':'Aziz', 'othername':'', 'constituency':'Kalaka', 'portfolio':''},
            {'name':'Ali_Biju'                              , 'firstname':'Ali'             , 'lastname':'Biju', 'othername':'', 'constituency':'Krian', 'portfolio':''},
            {'name':'Mohamad_Chee_Kadir'                    , 'firstname':'Mohamad Chee'    , 'lastname':'Kadir', 'othername':'', 'constituency':'Kabong', 'portfolio':''},
            {'name':'Len_Talif_Saleh'                       , 'firstname':'Len Talif'       , 'lastname':'Saleh', 'othername':'', 'constituency':'Kuala Rajang', 'portfolio':''},
            {'name':'Abdullah_Saidol'                       , 'firstname':'Abdullah'        , 'lastname':'Saidol', 'othername':'', 'constituency':'Semop', 'portfolio':''},
            {'name':'Safiee_Ahmad'                          , 'firstname':'Safiee'          , 'lastname':'Ahmad', 'othername':'', 'constituency':'Daro', 'portfolio':''},
            {'name':'Juanda_Jaya'                           , 'firstname':'Juanda'          , 'lastname':'Jaya', 'othername':'', 'constituency':'Jemoreng', 'portfolio':''},
#            {'name':''                       , 'firstname':''       , 'lastname':'', 'othername':'', 'constituency':'', 'portfolio':''},
#            {'name':''                       , 'firstname':''       , 'lastname':'', 'othername':'', 'constituency':'', 'portfolio':''},
#            {'name':''                       , 'firstname':''       , 'lastname':'', 'othername':'', 'constituency':'', 'portfolio':''},
        ]
        for obj in politicians:
            constituency = Constituency.objects.filter(name=obj['constituency']).get()
            politician, created = Politician.objects.get_or_create(name=obj['name'], firstname=obj['firstname'], lastname=obj['lastname'], othername=obj['othername'])
            politician.constituency.add(constituency)
            if obj['portfolio'] != '':
                for portfolio in obj['portfolio']:
                    pf = Portfolio.objects.get(name=portfolio)
                    politician.portfolio.add(pf)
        self.stdout.write(self.style.SUCCESS('Success adding politicians.') )

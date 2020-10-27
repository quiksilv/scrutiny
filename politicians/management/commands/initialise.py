from django.core.management.base import BaseCommand, CommandError
from politicians.models import Party, Constituency, Portfolio, Politician

class Command(BaseCommand):
    help = 'Initialise with preloaded data'
    def add_arguments(self, parser):
        parser.add_argument('--state', type=str, help='Initialise state data. Currently sarawak and federal only.')
    def handle(self, *args, **options):
        if not options['state']:
            self.stdout.write(self.style.WARNING('Not enough arguments.') )
        if options['state'] == 'federal':
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
        if options['state'] == 'sarawak':
            parties = [
                {'abbr': 'IND', 'english_name': 'Independent', 'malay_name': '', 'chinese_name': '', 'iban_name': '', 'tamil_name': ''},
                {'abbr': 'SUPP', 'english_name': 'Sarawak United Peoples\' Party', 'malay_name': 'Parti Rakyat Bersatu Sarawak', 'chinese_name': '砂拉越人民联合党', 'iban_name': 'Gerempong Sa\'ati Rayat Sarawak', 'tamil_name': ''},
                {'abbr': 'PBB', 'english_name': 'United Traditional Bumiputera Party', 'malay_name': 'Parti Pesaka Bumiputera Bersatu', 'chinese_name': '砂拉越土著保守联合党', 'iban_name': '', 'tamil_name': ''},
                {'abbr': 'PDP', 'english_name': 'Progressive Democratic Party', 'malay_name': 'Parti Demokratik Progresif', 'chinese_name': '民主进步党', 'iban_name': '', 'tamil_name': ''},
                {'abbr': 'PRS', 'english_name': 'Sarawak Peoples\' Party', 'malay_name': 'Parti Rakyat Sarawak', 'chinese_name': '', 'iban_name': '', 'tamil_name': ''},
                {'abbr': 'DAP', 'english_name': 'Democratic Action Party', 'malay_name': 'Parti Tindakan Demokratik', 'chinese_name': '民主行動黨', 'iban_name': '', 'tamil_name': 'ஜனநாயக செயல் கட்சி'},
                {'abbr': 'PKR', 'english_name': 'People\'s Justice Party', 'malay_name': 'Parti Keadilan Rakyat', 'chinese_name': '人民公正黨', 'iban_name': '', 'tamil_name': 'மக்கள் நீதி கட்சி'},
                {'abbr': 'PSB', 'english_name': 'United Sarawak Party', 'malay_name': 'Parti Sarawak Bersatu', 'chinese_name': '砂拉越團結黨', 'iban_name': '', 'tamil_name': ''},
                {'abbr': 'BERSATU', 'english_name': 'Malaysian United Indigenous Party', 'malay_name': 'Parti Pribumi Bersatu Malaysia', 'chinese_name': '马来西亚土著团结党', 'iban_name': '', 'tamil_name': 'பிபிபீஏம் (மலேசிய ஐக்கிய மக்கள் கட்சி)'},
            ]
            for party in parties:
                Party.objects.update_or_create(abbr=party['abbr'], english_name=party['english_name'], malay_name=party['malay_name'], chinese_name=party['chinese_name'], iban_name=party['iban_name'])
            self.stdout.write(self.style.SUCCESS('Success adding parties.') )
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
                Constituency.objects.update_or_create(state='Sarawak', code=obj['code'], name=obj['name'])
            self.stdout.write(self.style.SUCCESS('Success adding constituencies.') )
    
            portfolios = [
                {'name': 'Chief Minister', 'othername': '首席部长'},
                {'name': 'Minister of Finance and Economic Planning', 'othername': '财政及经济策划部部长'},
                {'name': 'Minister of Urban Development and Resources', 'othername': '城市发展及天然资源部部长'},
                {'name': 'Deputy Chief Minister', 'othername': '副首席部长'},
                {'name': 'Minister of Agriculture, Native Land and Regional Development', 'othername': '农业现代化、土著地及区域发展部部长'},
                {'name': 'Assistant Minister for Native Laws and Customs', 'othername': '首长署助理部长（土著法律及习俗）'},
                {'name': 'Assistant Minister for Law, State-Federal Relations and Project Monitoring', 'othername': '首长署助理部长（法律、州及联邦关系及计划监督）'},
                {'name': 'Assistant Minister for Corporate Affairs', 'othername': '首长署助理部长（企业事务）'},
                {'name': 'Assistant Minister for Urban Planning, Land Administration and Environment', 'othername': '城市发展及天然资源部助理部长（城市发展、土地行政及环境）'},
                {'name': 'Assistant Minister for Native Land Development', 'othername': '农业现代化、土著地及区域发展部助理部长（土著地发展）'},
                {'name': 'Assistant Minister for Agriculture', 'othername': '农业现代化、土著地及区域发展部助理部长（农业）'},
                {'name': 'Assistant Minister for Coastal Road', 'othername': '基本设施发展及交通部助理部长（沿海道路）'},
                {'name': 'Assistant Minister for Transportation', 'othername': '基本设施发展及交通部助理部长（交通）'},
                {'name': 'Assistant Minister for Entrepreneur and Small Medium Enterprise Development', 'othername': '工业及企业发展部助理部长（企业及中小型企业发展）'},
                {'name': 'Assistant Minister for E-Commerce', 'othername': '国际贸易及电子商务部助理部长（电子商务）'},
                {'name': 'Assistant Minister for Education and Technological Research', 'othername': '教育、科学及工艺研究部助理部长（教育及工艺研究）'},
                {'name': 'Assistant Minister for Community Well-being', 'othername': '福利、社区和谐、妇女、家庭及儿童发展部助理部长（社区和谐）'},
                {'name': 'Assistant Minister for Women, Family and Childhood Development', 'othername': '福利、社区和谐、妇女、家庭及儿童发展部助理部长（妇女、家庭及儿童发展部）'},
                {'name': 'Assistant Minister for Local Government and Housing', 'othername': '地方政府及房屋部助理部长（地方政府）'},
                {'name': 'Assistant Minister for Housing and Public Health', 'othername': '地方政府及房屋部助理部长（房屋及公共卫生）'},
                {'name': 'Assistant Minister for Water Supply', 'othername': '乡区电力及水供部助理部长（水供）'},
                {'name': 'Assistant Minister for Rural Electricity', 'othername': '乡区电力及水供部助理部长（乡区电力）'},
                {'name': 'Assistant Minister for Tourism, Art and Culture', 'othername': '旅游、艺术、文化、青年及体育部助理部长（旅游、艺术及文化部）'},
                {'name': 'Assistant Minister for Youth and Sports', 'othername': '旅游、艺术、文化、青年及体育部助理部长（青年及体育）'},
                {'name': 'Assistant Minister for Industries and Investment', 'othername': '工业及企业发展部助理部长（工业及投资）'},
                {'name': 'Second Minister of Finance', 'othername': '第二财政部长'},
                {'name': 'Minister of Infrastructural and Ports Development', 'othername': '基本设施发展及交通部部长'},
                {'name': 'Minister of International Trade and Industry, Industrial Terminal and Entrepreneur Development', 'othername': '工业及企业发展部部长'},
                {'name': 'Second Minister of Urban Development and Resources', 'othername': '第二城市发展及资源部长'},
                {'name': 'Minister in the Chief Minister\'s Office', 'othername': '首长署部长'},
                {'name': 'Minister of Education, Science and Technological Research', 'othername': '教育、科学及工艺研究部部长'},
                {'name': 'Minister of Local Government and Housing', 'othername': '地方政府及房屋部部长'},
                {'name': 'Minister of Tourism, Art, Culture', 'othername': '旅游、艺术、文化、青年及体育部部长'},
                {'name': 'Minister of Youth and Sports', 'othername': '青年及体育部部长'},
                {'name': 'Minister of Transport', 'othername': '交通部部长'},
                {'name': 'Minister of Utilities', 'othername': '乡区电力及水供部部长'},
                {'name': 'Minister of Welfare, Community Well-being, Women, Family and Childhood Development', 'othername': '福利、社区和谐、妇女、家庭及儿童发展部部长'},
                {'name': 'Speaker', 'othername': ''},
                {'name': 'Deputy Speaker', 'othername': ''},
                {'name': 'Opposition Leader', 'othername': ''},
            ]
            for obj in portfolios:
                if Portfolio.objects.filter(name=obj['name']).count():
                    Portfolio.objects.filter(name=obj['name']).update(othername=obj['othername'])
                else:
                    Portfolio.objects.create(name=obj['name'], othername=obj['othername'])
            self.stdout.write(self.style.SUCCESS('Success adding portfolios.') )
            politicians = [
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=764', 'party': 'PSB', 'name':'Ranum_Mina'                            , 'firstname':'Ranum'           , 'lastname':'Mina'                 , 'othername':''           , 'facebook':'', 'constituency':'Opar'         , 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=765', 'party': 'PDP', 'name':'Henry_Harry_Jinep'                     , 'firstname':'Henry Harry'     , 'lastname':'Jinep'                , 'othername':''           , 'facebook':'', 'constituency':'Tasik Biru'   , 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=766', 'party': 'PBB', 'name':'Jamilah_Anu'                           , 'firstname':'Jamilah'         , 'lastname':'Anu'                  , 'othername':''           , 'facebook':'', 'constituency':'Tanjung Datu' , 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=767', 'party': 'PBB', 'name':'Abdul_Rahman_Junaidi'                  , 'firstname':'Abdul Rahman'    , 'lastname':'Junaidi'              , 'othername':'阿都拉曼朱乃迪', 'facebook':'', 'constituency':'Pantai Damai' , 'portfolio':['Assistant Minister for Rural Electricity']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=768', 'party': 'PBB', 'name':'Hazland_Abang_Hipni'                   , 'firstname':'Hazland'         , 'lastname':'Abang Hipni'          , 'othername':''           , 'facebook':'', 'constituency':'Demak Laut'   , 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=769', 'party': 'PBB', 'name':'Fazzrudin_Abdul_Rahman'                , 'firstname':'Fazzrudin'       , 'lastname':'Abdul Rahman'         , 'othername':''           , 'facebook':'', 'constituency':'Tupong'       , 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=770', 'party': 'PBB', 'name':'Sharifah_Hasidah_Sayeed_Aman_Ghazali'  , 'firstname':'Sharifah Hasidah', 'lastname':'Sayeed Aman Ghazali'  , 'othername':'莎丽花茜达'     , 'facebook':'', 'constituency':'Samariang', 'portfolio':['Assistant Minister for Law, State-Federal Relations and Project Monitoring']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=850', 'party': 'PBB', 'name':'Abang_Abdul_Rahman_Zohari_Abang_Openg'  , 'firstname':'Abang_Abdul Rahman Zohari', 'lastname':'Abang Openg', 'othername':'阿邦佐哈里'   , 'facebook':'', 'constituency':'Satok', 'portfolio':['Chief Minister', 'Minister of Finance and Economic Planning', 'Minister of Urban Development and Resources']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=772', 'party': 'DAP', 'name':'Wong_King_Wei'                         , 'firstname':'King Wei'        , 'lastname':'Wong'                 , 'othername':'黄庆伟'     , 'facebook':'wongkingweipage', 'constituency':'Padungan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=773', 'party': 'DAP', 'name':'Violet_Yong_Wui_Wui'                   , 'firstname':'Wui Wui'         , 'lastname':'Yong'                 , 'othername':'杨薇讳'     , 'facebook':'violet.yong.1', 'constituency':'Pending', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=774', 'party': 'PSB', 'name':'See_Chee_How'                          , 'firstname':'Chee How'        , 'lastname':'See'                  , 'othername':'施志豪'     , 'facebook':'SCheeHow', 'constituency':'Batu Lintang', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=775', 'party': 'DAP', 'name':'Chong_Chieng_Jen'                      , 'firstname':'Chieng Jen'      , 'lastname':'Chong'                , 'othername':'张健仁'     , 'facebook': 'ChongChiengJen', 'constituency':'Kota Sentosa', 'portfolio':['Opposition Leader']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=776', 'party': 'SUPP', 'name':'Lo_Khere_Chiang'                       , 'firstname':'Khere Chiang'    , 'lastname':'Lo'                  , 'othername':'罗克强'     , 'facebook': 'LoKhereChiang', 'constituency':'Batu Kitang', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=777', 'party': 'SUPP', 'name':'Sim_Kui_Hian'                          , 'firstname':'Kui Hian'        , 'lastname':'Sim'                 , 'othername':'沈桂贤'     , 'facebook': 'dr.sim.kui.hian', 'constituency':'Batu Kawah', 'portfolio':['Minister of Local Government and Housing']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=778', 'party': 'PBB', 'name':'Abdul_Karim_Rahman_Hamzah'             , 'firstname':'Abdul Karim'     , 'lastname':'Rahman Hamzah'        , 'othername':'阿都卡林', 'facebook':'', 'constituency':'Asajaya', 'portfolio':['Minister of Tourism, Art, Culture', 'Minister of Youth and Sports']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=779', 'party': 'PBB', 'name':'Idris_Buang'                           , 'firstname':'Idris'           , 'lastname':'Buang'                , 'othername':'', 'facebook':'', 'constituency':'Muara Tuang', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=780', 'party': 'PBB', 'name':'Mohammad_Ali_Mahmud'                   , 'firstname':'Mohammad Ali'    , 'lastname':'Mahmud'               , 'othername':'', 'facebook':'', 'constituency':'Stakan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=781', 'party': 'PBB', 'name':'Miro_Simuh'                            , 'firstname':'Miro'            , 'lastname':'Simuh'                , 'othername':'', 'facebook':'', 'constituency':'Serembu', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=782', 'party': 'SUPP', 'name':'Jerip_Susil'                           , 'firstname':'Jerip'           , 'lastname':'Susil'               , 'othername':'哲历苏西尔', 'facebook':'', 'constituency':'Mambong', 'portfolio':['Assistant Minister for Transportation']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=783', 'party': 'PBB', 'name':'Roland_Sagah_Wee_Inn'                  , 'firstname':'Roland Sagah'    , 'lastname':'Wee Inn'              , 'othername':'罗伦沙嘉', 'facebook':'', 'constituency':'Tarat', 'portfolio':['Assistant Minister for Native Land Development']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=784', 'party': 'PBB', 'name':'Michael_Manyin_Jawong'                 , 'firstname':'Micheal Manyin'  , 'lastname':'Jawong'               , 'othername':'', 'facebook':'', 'constituency':'Tebedu', 'portfolio':['Minister of Education, Science and Technological Research']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=785', 'party': 'PBB', 'name':'Maclaine_Ben'                          , 'firstname':'Maclaine'        , 'lastname':'Ben'                  , 'othername':'', 'facebook':'', 'constituency':'Kedup', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=786', 'party': 'PBB', 'name':'John_Ilus'                             , 'firstname':'John'            , 'lastname':'Ilus'                 , 'othername':'', 'facebook':'', 'constituency':'Bukit Semuja', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=787', 'party': 'PBB', 'name':'Aidel_Lariwoo'                         , 'firstname':'Aidel'           , 'lastname':'Lariwoo'              , 'othername':'', 'facebook':'', 'constituency':'Sadong Jaya', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=788', 'party': 'PBB', 'name':'Awla_Dris'                             , 'firstname':'Awla'            , 'lastname':'Dris'                 , 'othername':'', 'facebook':'', 'constituency':'Simunjan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=789', 'party': 'PBB', 'name':'Mohd_Naroden_Majais'                   , 'firstname':'Mohd Naroden'    , 'lastname':'Majais'               , 'othername':'莫哈末纳鲁丁', 'facebook':'', 'constituency':'Gedong', 'portfolio':['Assistant Minister for Entrepreneur and Small Medium Enterprise Development', 'Assistant Minister for E-Commerce']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=790', 'party': 'PBB', 'name':'Julaihi_Narawi'                        , 'firstname':'Julaihi'         , 'lastname':'Narawi'               , 'othername':'朱莱希诺拉威', 'facebook':'', 'constituency':'Sebuyau', 'portfolio':['Assistant Minister for Coastal Road']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=792', 'party': 'PBB', 'name':'Simoi_Peri'                            , 'firstname':'Simoi'           , 'lastname':'Peri'                 , 'othername':'', 'facebook':'', 'constituency':'Lingga', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=793', 'party': 'PBB', 'name':'Razaili_Gapor'                         , 'firstname':'Razaili'         , 'lastname':'Gapor'                , 'othername':'', 'facebook':'', 'constituency':'Beting Maro', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=849', 'party': 'PRS', 'name':'Snowdan_Lawan'                         , 'firstname':'Snowdan'         , 'lastname':'Lawan'                , 'othername':'史诺丹拉旺', 'facebook':'', 'constituency':'Balai Ringin', 'portfolio':['Assistant Minister for Youth and Sports']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=795', 'party': 'PRS', 'name':'Mong_Dagang'                           , 'firstname':'Mong'            , 'lastname':'Dagang'               , 'othername':'', 'facebook':'', 'constituency':'Bukit Begunan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=796', 'party': 'SUPP', 'name':'Francis_Harden_Hollis'                 , 'firstname':'Francis Harden'  , 'lastname':'Hollis'              , 'othername':'法兰斯哈丁', 'facebook':'', 'constituency':'Simanggang', 'portfolio':['Assistant Minister for Community Well-being']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=797', 'party': 'PSB', 'name':'Johnical_Rayong_Ngipa'                , 'firstname':'Johnical'        , 'lastname':'Ngipa'                 , 'othername':'', 'facebook':'', 'constituency':'Engkilili', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=798', 'party': 'PRS', 'name':'Malcom_Mussen_Lamoh'                   , 'firstname':'Malcom Mussen'   , 'lastname':'Lamoh'                , 'othername':'麦康莫森', 'facebook':'', 'constituency':'Batang Ai', 'portfolio':['Assistant Minister for Industries and Investment']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=799', 'party': 'PBB', 'name':'Mohammad_Razi_Sitam'                   , 'firstname':'Mohammad Razi'   , 'lastname':'Sitam'                , 'othername':'', 'facebook':'', 'constituency':'Saribas', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=800', 'party': 'PBB', 'name':'Gerald_Rentap_Jabu'                    , 'firstname':'Gerald Rentap'   , 'lastname':'Jabu'                 , 'othername':'', 'facebook':'', 'constituency':'Layar', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=801', 'party': 'PBB', 'name':'Douglas_Uggah_Embas'                   , 'firstname':'Douglas Uggah'   , 'lastname':'Embas'                , 'othername':'道格拉斯乌加恩巴斯', 'facebook':'douglasuggah.embas', 'constituency':'Bukit Saban', 'portfolio':['Deputy Chief Minister', 'Minister of Agriculture, Native Land and Regional Development', 'Second Minister of Finance']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=802', 'party': 'PBB', 'name':'Abdul_Wahab_Aziz'                      , 'firstname':'Abdul Wahab'     , 'lastname':'Aziz'                 , 'othername':'', 'facebook':'', 'constituency':'Kalaka', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=803', 'party': 'BERSATU', 'name':'Ali_Biju'                          , 'firstname':'Ali'             , 'lastname':'Biju'                 , 'othername':'', 'facebook':'', 'constituency':'Krian', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=804', 'party': 'PBB', 'name':'Mohamad_Chee_Kadir'                    , 'firstname':'Mohamad Chee'    , 'lastname':'Kadir'                , 'othername':'', 'facebook':'', 'constituency':'Kabong', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=805', 'party': 'PBB', 'name':'Len_Talif_Saleh'                       , 'firstname':'Len Talif'       , 'lastname':'Saleh'                , 'othername':'连达立夫', 'facebook':'', 'constituency':'Kuala Rajang', 'portfolio':['Assistant Minister for Urban Planning, Land Administration and Environment']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=806', 'party': 'PBB', 'name':'Abdullah_Saidol'                       , 'firstname':'Abdullah'        , 'lastname':'Saidol'               , 'othername':'莎丽花茜达', 'facebook':'', 'constituency':'Semop', 'portfolio':['Assistant Minister for Corporate Affairs']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=807', 'party': 'PBB', 'name':'Safiee_Ahmad'                          , 'firstname':'Safiee'          , 'lastname':'Ahmad'                , 'othername':'', 'facebook':'', 'constituency':'Daro', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=808', 'party': 'PBB', 'name':'Juanda_Jaya'                           , 'firstname':'Juanda'          , 'lastname':'Jaya'                 , 'othername':'', 'facebook':'', 'constituency':'Jemoreng', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=809', 'party': 'SUPP', 'name':'Huang_Tiong_Sii'                      , 'firstname':'Tiong Sii'       , 'lastname':'Huang'                , 'othername':'范长钖', 'facebook':'suppn45repok', 'constituency':'Repok', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=810', 'party': 'SUPP', 'name':'Ding_Kuong_Hiing'                     , 'firstname':'Kuong Hiing'     , 'lastname':'Ding'                 , 'othername':'陈冠勋', 'facebook':'DUNN46Meradong', 'constituency':'Meradong', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=811', 'party': 'PBB', 'name':'William_Mawan_Ikom'                    , 'firstname':'William Mawan'   , 'lastname':'Ikom'                 , 'othername':'', 'facebook': '', 'constituency':'Pakan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=812', 'party': 'PDP', 'name':'Rolland_Duat_Jubin'                    , 'firstname':'Rolland Duat'    , 'lastname':'Jubin'                , 'othername':'', 'facebook': '', 'constituency':'Meluan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=813', 'party': 'PRS', 'name':'Alexander_Vincent'                     , 'firstname':'Alexander'       , 'lastname':'Vincent'              , 'othername':'', 'facebook': '', 'constituency':'Ngemah', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=814', 'party': 'PBB', 'name':'Allan_Siden_Gramong'                   , 'firstname':'Allan Siden'     , 'lastname':'Gramong'              , 'othername':'', 'facebook': '', 'constituency':'Machan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=815', 'party': 'DAP', 'name':'Irene_Mary_Chang_Oi_Ling'              , 'firstname':'Oi Ling'         , 'lastname':'Chang'                , 'othername':'郑爱鸰', 'facebook': 'irenedapsibu', 'constituency':'Bukit Assek', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=816', 'party': 'PSB', 'name':'Tiong_Thai_King'                       , 'firstname':'Thai King'       , 'lastname':'Tiong'                , 'othername':'张泰卿', 'facebook': '', 'constituency':'Dudong', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=817', 'party': 'PSB', 'name':'Wong_Soon_Koh'                         , 'firstname':'Soon Koh'        , 'lastname':'Wong'                 , 'othername':'黄顺舸', 'facebook': '', 'constituency':'Bawang Assan', 'portfolio':['Second Minister of Finance', 'Minister of International Trade and E-commerce']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=818', 'party': 'DAP', 'name':'Wong_Kee_Woan'                         , 'firstname':'Kee Woan'        , 'lastname':'Wong'                 , 'othername':'黄培根', 'facebook': 'wongkeewoan', 'constituency':'Pelawan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=819', 'party': 'PBB', 'name':'Annuar_Rapaee'                         , 'firstname':'Annuar'          , 'lastname':'Rapaee'               , 'othername':'安华拉拜', 'facebook':'', 'constituency':'Nangka', 'portfolio':['Assistant Minister for Education and Technological Research', 'Assistant Minister for Housing and Public Health']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=851', 'party': 'PBB', 'name':'Fatimah_Abdullah'                      , 'firstname':'Fatimah'         , 'lastname':'Abdullah'             , 'othername':'花蒂玛阿都拉', 'facebook':'', 'constituency':'Dalat', 'portfolio':['Minister of Welfare, Community Well-being, Women, Family and Childhood Development']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=821', 'party': 'PBB', 'name':'Yussibnosh_Balo'                       , 'firstname':'Yussibnosh'      , 'lastname':'Balo'                 , 'othername':'', 'facebook':'', 'constituency':'Tellian', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=822', 'party': 'PBB', 'name':'Abdul_Yakub_Arbi'                      , 'firstname':'Abdul Yakub'     , 'lastname':'Arbi'                 , 'othername':'', 'facebook':'', 'constituency':'Balingian', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=823', 'party': 'PRS', 'name':'Christopher_Gira_Sambang'              , 'firstname':'Christopher Gira', 'lastname':'Sambang'              , 'othername':'', 'facebook':'', 'constituency':'Tamin', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=824', 'party': 'PRS', 'name':'John_Sikie_Tayai'                      , 'firstname':'John Sikie'      , 'lastname':'Tayai'                , 'othername':'约翰西基', 'facebook':'', 'constituency':'Kakus', 'portfolio':['Assistant Minister for Native Laws and Customs']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=825', 'party': 'PRS', 'name':'Wilson_Nyabong_Ijang'                  , 'firstname':'Wilson Nyabong'  , 'lastname':'Ijang'                , 'othername':'', 'facebook':'', 'constituency':'Pelagus', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=826', 'party': 'PBB', 'name':'Ambrose_Blikau_Enturan'                , 'firstname':'Ambrose Blikau'  , 'lastname':'Enturan'              , 'othername':'', 'facebook':'', 'constituency':'Katibas', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=827', 'party': 'PBB', 'name':'Jefferson_Jamit_Unyat'                 , 'firstname':'Jefferson Jamit' , 'lastname':'Unyat'                , 'othername':'', 'facebook':'', 'constituency':'Bukit Goram', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=828', 'party': 'PRS', 'name':'James_Jemut_Masing'                    , 'firstname':'James Jemut'     , 'lastname':'Masing'               , 'othername':'詹姆斯玛欣', 'facebook':'', 'constituency':'Baleh', 'portfolio':['Deputy Chief Minister', 'Minister of Infrastructural and Ports Development']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=852', 'party': 'PRS', 'name':'Liwan_Lagang'                          , 'firstname':'Liwan'           , 'lastname':'Lagang'               , 'othername':'里旺拉岗', 'facebook':'', 'constituency':'Belaga', 'portfolio':['Assistant Minister for Water Supply']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=830', 'party': 'PRS', 'name':'Chukpai_Ugon'                          , 'firstname':'Chukpai'         , 'lastname':'Ugon'                 , 'othername':'', 'facebook':'', 'constituency':'Murum', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=831', 'party': 'PBB', 'name':'Talib_Zulpilip'                        , 'firstname':'Talib'           , 'lastname':'Zulpilip'             , 'othername':'达立朱菲立', 'facebook':'', 'constituency':'Jepak', 'portfolio':['Minister in the Chief Minister\'s Office']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=832', 'party': 'DAP', 'name':'Chiew_Chiu_Sing'                       , 'firstname':'Chiu Sing'       , 'lastname':'Chiew'                , 'othername':'', 'facebook':'chinsing.chiew', 'constituency':'Tanjong Batu', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=833', 'party': 'PBB', 'name':'Stephen_Rundi_Utom'                    , 'firstname':'Stephen Rundi'   , 'lastname':'Utom'                 , 'othername':'史蒂芬伦迪', 'facebook':'', 'constituency':'Kemena', 'portfolio':['Minister of Utilities']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=834', 'party': 'PRS', 'name':'Majang_Renggi'                         , 'firstname':'Majang'          , 'lastname':'Renggi'               , 'othername':'', 'facebook':'', 'constituency':'Samalaju', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=835', 'party': 'PBB', 'name':'Rosey_Yunus'                           , 'firstname':'Rosey'           , 'lastname':'Yunus'                , 'othername':'罗茜', 'facebook':'', 'constituency':'Bekenu', 'portfolio':['Assistant Minister for Women, Family and Childhood Development']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=836', 'party': 'PBB', 'name':'Ripin_Lamat'                           , 'firstname':'Ripin'           , 'lastname':'Lamat'                , 'othername':'', 'facebook':'', 'constituency':'Lambir', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=837', 'party': 'SUPP', 'name':'Sebastian_Ting_Chiew_Yew'             , 'firstname':'Chiew Yew'       , 'lastname':'Ting'                 , 'othername':'陳超耀', 'facebook':'SebastianTing8188', 'constituency':'Piasau', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=838', 'party': 'SUPP', 'name':'Lee_Kim_Shin'                         , 'firstname':'Kim Shin'        , 'lastname':'Lee'                  , 'othername':'李景胜', 'facebook':'leekimshinsenadin', 'constituency':'Senadin', 'portfolio':['Minister of Transport']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=839', 'party': 'PDP', 'name':'Penguang_Manggil'                      , 'firstname':'Penguang'        , 'lastname':'Manggil'              , 'othername':'朋光曼吉', 'facebook':'', 'constituency':'Marudi', 'portfolio':['Assistant Minister for Local Government and Housing']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=840', 'party': 'PBB', 'name':'Dennis_Ngau'                           , 'firstname':'Dennis'          , 'lastname':'Ngau'                 , 'othername':'', 'facebook':'', 'constituency':'Telang Usan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=841', 'party': 'PBB', 'name':'Gerawat_Gala'                          , 'firstname':'Gerawat'         , 'lastname':'Gala'                 , 'othername':'', 'facebook':'', 'constituency':'Mulu', 'portfolio':['Deputy Speaker']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=842', 'party': 'PBB', 'name':'Abdul_Rahman_Ismail'                   , 'firstname':'Abdul Rahman'    , 'lastname':'Ismail'               , 'othername':'阿都拉曼依斯迈', 'facebook':'', 'constituency':'Bukit Kota', 'portfolio':['Assistant Minister for Agriculture']},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=843', 'party': 'PBB', 'name':'Paulus_Palu_Gumbang'                   , 'firstname':'Paulus Palu'     , 'lastname':'Gumbang'              , 'othername':'', 'facebook':'', 'constituency':'Batu Danau', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=844', 'party': 'PSB', 'name':'Baru_Bian'                             , 'firstname':'Baru'            , 'lastname':'Bian'                 , 'othername':'巴鲁比安', 'facebook':'barubian', 'constituency':'Ba\'kelalan', 'portfolio':''},
                {'image_url': 'https://duns.sarawak.gov.my/modules/web/image_show.php?id=845', 'party': 'PBB', 'name':'Awang_Tengah_Ali_Hasan'                , 'firstname':'Awang Tengah'    , 'lastname':'Ali Hasan'            , 'othername':'阿旺登雅', 'facebook':'', 'constituency':'Bukit Sari', 'portfolio':['Deputy Chief Minister', 'Minister of International Trade and Industry, Industrial Terminal and Entrepreneur Development', 'Second Minister of Urban Development and Resources']},
            ]
            for obj in politicians:
                party = Party.objects.get(abbr=obj['party'])
                if Politician.objects.filter(name=obj['name']).count():
                    politician = Politician.objects.filter(name=obj['name']).update(image_url=obj['image_url'], party=party, firstname=obj['firstname'], lastname=obj['lastname'], othername=obj['othername'], facebook=obj['facebook'])
                else:
                    politician = Politician.objects.create(image_url=obj['image_url'], party=party, name=obj['name'], firstname=obj['firstname'], lastname=obj['lastname'], othername=obj['othername'], facebook=obj['facebook'])
                    Constituency.objects.filter(name=obj['constituency']).update(politician=politician)
                    if obj['portfolio'] != '':
                        for portfolio in obj['portfolio']:
                            Portfolio.objects.filter(name=portfolio).update(politician=politician)
            self.stdout.write(self.style.SUCCESS('Success adding politicians.') )
            #sample twitter handle for testing
            Politician.objects.filter(name=obj['name']).update(twitter='simkuihian')

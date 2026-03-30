from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from main.models import Season, Club, Player, Transfer


class Command(BaseCommand):
    help = 'Seed real transfer data into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing transfers and seasons before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Transfer.objects.all().delete()
            Season.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all transfers and seasons.'))

        # --- Create Seasons ---
        seasons_data = [
            '2020/21',
            '2021/22',
            '2022/23',
            '2023/24',
            '2024/25',
        ]
        seasons = {}
        for s in seasons_data:
            obj, _ = Season.objects.get_or_create(name=s)
            seasons[s] = obj
        self.stdout.write(self.style.SUCCESS(f'Seasons ready: {len(seasons)}'))

        # --- Transfer Data ---
        # Format: (player_name, club_from_name, club_to_name, season_name, price, tft_price, date)
        transfers_data = [
            # ===== 2021/22 — ORIGINAL =====
            ('Romelu Lukaku',         'Inter Milan',           'Chelsea',               '2021/22', 115.00, 110.00, '2021-08-12'),
            ('Jadon Sancho',          'Borussia Dortmund',     'Manchester United',     '2021/22',  85.00,  80.00, '2021-07-23'),
            ('Jack Grealish',         'Aston Villa',           'Manchester City',       '2021/22', 117.50, 115.00, '2021-08-05'),
            ('Lionel Messi',          'Barcelona',             'Paris Saint-Germain',   '2021/22',   0.00,   0.00, '2021-08-10'),
            ('Sergio Ramos',          'Real Madrid',           'Paris Saint-Germain',   '2021/22',   0.00,   0.00, '2021-07-01'),
            ('Raphael Varane',        'Real Madrid',           'Manchester United',     '2021/22',  47.00,  45.00, '2021-08-14'),
            ('Achraf Hakimi',         'Inter Milan',           'Paris Saint-Germain',   '2021/22',  68.00,  65.00, '2021-07-06'),
            ('Georginio Wijnaldum',   'Liverpool',             'Paris Saint-Germain',   '2021/22',   0.00,   0.00, '2021-07-01'),
            ('Dusan Vlahovic',        'Fiorentina',            'Juventus',              '2021/22',  80.00,  75.00, '2022-01-28'),
            ('Bukayo Saka',           'Arsenal',               'Arsenal',               '2021/22',   0.00,   0.00, '2021-07-01'),
            ('Ben White',             'Brighton',              'Arsenal',               '2021/22',  57.00,  55.00, '2021-08-06'),
            ('Saul Niguez',           'Atletico Madrid',       'Chelsea',               '2021/22',   5.00,   4.50, '2021-08-31'),
            ('Tammy Abraham',         'Chelsea',               'AS Roma',               '2021/22',  40.00,  38.00, '2021-08-17'),
            ('Dayot Upamecano',       'RB Leipzig',            'Bayern Munich',         '2021/22',  42.50,  40.00, '2021-07-01'),
            ('Yves Bissouma',         'Brighton',              'Tottenham Hotspur',     '2021/22',  30.00,  28.00, '2022-06-01'),

            # ===== 2022/23 — ORIGINAL =====
            ('Erling Haaland',        'Borussia Dortmund',     'Manchester City',       '2022/23',  60.00,  58.00, '2022-07-01'),
            ('Darwin Nunez',          'Benfica',               'Liverpool',             '2022/23',  85.00,  80.00, '2022-06-13'),
            ('Raheem Sterling',       'Manchester City',       'Chelsea',               '2022/23',  56.20,  52.00, '2022-07-13'),
            ('Kalidou Koulibaly',     'Napoli',                'Chelsea',               '2022/23',  40.00,  38.00, '2022-07-20'),
            ('Matthijs de Ligt',      'Juventus',              'Bayern Munich',         '2022/23',  77.00,  72.00, '2022-07-26'),
            ('Sadio Mane',            'Liverpool',             'Bayern Munich',         '2022/23',  32.00,  30.00, '2022-06-22'),
            ('Casemiro',              'Real Madrid',           'Manchester United',     '2022/23',  70.65,  68.00, '2022-08-22'),
            ('Antony',                'Ajax',                  'Manchester United',     '2022/23',  95.00,  88.00, '2022-08-30'),
            ('Richarlison',           'Everton',               'Tottenham Hotspur',     '2022/23',  60.00,  55.00, '2022-07-01'),
            ('Gabriel Jesus',         'Manchester City',       'Arsenal',               '2022/23',  52.00,  50.00, '2022-07-04'),
            ('Lisandro Martinez',     'Ajax',                  'Manchester United',     '2022/23',  57.37,  55.00, '2022-07-27'),
            ('Marc Cucurella',        'Brighton',              'Chelsea',               '2022/23',  65.00,  60.00, '2022-08-15'),
            ('Wesley Fofana',         'Leicester City',        'Chelsea',               '2022/23',  80.40,  75.00, '2022-08-31'),
            ('Aurelien Tchouameni',   'Monaco',                'Real Madrid',           '2022/23',  80.00,  75.00, '2022-06-16'),
            ('Enzo Fernandez',        'Benfica',               'Chelsea',               '2022/23', 121.00, 115.00, '2023-01-31'),
            ('Joao Felix',            'Atletico Madrid',       'Chelsea',               '2022/23',  11.00,  10.00, '2023-01-12'),
            ('Malo Gusto',            'Lyon',                  'Chelsea',               '2022/23',  35.00,  33.00, '2023-01-26'),
            ('Leandro Trossard',      'Brighton',              'Arsenal',               '2022/23',  27.00,  25.00, '2023-01-13'),
            ('Cody Gakpo',            'PSV Eindhoven',         'Liverpool',             '2022/23',  44.00,  42.00, '2023-01-01'),
            ('Mykhaylo Mudryk',       'Shakhtar Donetsk',      'Chelsea',               '2022/23',  70.00,  65.00, '2023-01-12'),
            ('Noni Madueke',          'PSV Eindhoven',         'Chelsea',               '2022/23',  35.00,  33.00, '2023-01-26'),
            ('Benoit Badiashile',     'Monaco',                'Chelsea',               '2022/23',  38.00,  35.00, '2023-01-03'),
            ('David Neres',           'Shakhtar Donetsk',      'Benfica',               '2022/23',  15.00,  14.00, '2023-01-01'),
            ('Yannick Carrasco',      'Atletico Madrid',       'Al-Qadsiah',            '2022/23',  15.00,  14.00, '2023-01-30'),

            # ===== 2023/24 — ORIGINAL =====
            ('Declan Rice',           'West Ham United',       'Arsenal',               '2023/24', 116.60, 112.00, '2023-07-15'),
            ('Moises Caicedo',        'Brighton',              'Chelsea',               '2023/24', 116.62, 110.00, '2023-08-14'),
            ('Romeo Lavia',           'Southampton',           'Chelsea',               '2023/24',  58.00,  54.00, '2023-08-14'),
            ('Harry Kane',            'Tottenham Hotspur',     'Bayern Munich',         '2023/24', 100.00,  95.00, '2023-08-12'),
            ('Rasmus Hojlund',        'Atalanta',              'Manchester United',     '2023/24',  72.00,  68.00, '2023-08-05'),
            ('Andre Onana',           'Inter Milan',           'Manchester United',     '2023/24',  47.20,  44.00, '2023-07-18'),
            ('Khvicha Kvaratskhelia', 'Napoli',                'Paris Saint-Germain',   '2023/24',  70.00,  68.00, '2024-01-24'),
            ('Jude Bellingham',       'Borussia Dortmund',     'Real Madrid',           '2023/24', 103.00, 100.00, '2023-06-14'),
            ('Mason Mount',           'Chelsea',               'Manchester United',     '2023/24',  64.00,  60.00, '2023-07-05'),
            ('Nicolo Barella',        'Inter Milan',           'Chelsea',               '2023/24',  70.00,  68.00, '2024-01-01'),
            ('Sandro Tonali',         'AC Milan',              'Newcastle United',      '2023/24',  70.00,  65.00, '2023-07-31'),
            ('Ruben Neves',           'Wolverhampton',         'Al-Hilal',              '2023/24',  55.00,  50.00, '2023-07-04'),
            ("N'Golo Kante",          'Chelsea',               'Al-Ittihad',            '2023/24',   0.00,   0.00, '2023-07-01'),
            ('Karim Benzema',         'Real Madrid',           'Al-Ittihad',            '2023/24',   0.00,   0.00, '2023-07-01'),
            ('Neymar Jr',             'Paris Saint-Germain',   'Al-Hilal',              '2023/24',  90.00,  85.00, '2023-08-15'),
            ('Leny Yoro',             'Lille',                 'Manchester United',     '2024/25',  62.00,  60.00, '2024-07-22'),
            ('Michael Olise',         'Crystal Palace',        'Bayern Munich',         '2024/25',  53.00,  50.00, '2024-07-15'),
            ('Rodrigo',               'Manchester City',       'Al-Qadsiah',            '2023/24',   0.00,   0.00, '2024-08-05'),
            ('Manuel Akanji',         'Borussia Dortmund',     'Manchester City',       '2022/23',  17.50,  16.00, '2022-09-01'),
            ('Ilkay Gundogan',        'Manchester City',       'Barcelona',             '2023/24',   0.00,   0.00, '2023-07-01'),
            ('Gavi',                  'Barcelona',             'Barcelona',             '2023/24',   0.00,   0.00, '2023-07-01'),
            ('Pedri',                 'Barcelona',             'Barcelona',             '2023/24',   0.00,   0.00, '2023-07-01'),
            ('Robert Lewandowski',    'Bayern Munich',         'Barcelona',             '2022/23',  45.00,  42.00, '2022-07-19'),
            ('Raphinha',              'Leeds United',          'Barcelona',             '2022/23',  58.00,  55.00, '2022-07-15'),
            ('Jules Kounde',          'Sevilla',               'Barcelona',             '2022/23',  50.00,  48.00, '2022-07-23'),

            # ===== 2024/25 — ORIGINAL =====
            ('Joao Neves',            'Benfica',               'Paris Saint-Germain',   '2024/25',  73.00,  70.00, '2024-07-24'),
            ('Kylian Mbappe',         'Paris Saint-Germain',   'Real Madrid',           '2024/25',   0.00,   0.00, '2024-07-01'),
            ('Jadon Sancho',          'Manchester United',     'Chelsea',               '2024/25',  25.00,  22.00, '2025-01-27'),
            ('Marcus Rashford',       'Manchester United',     'Aston Villa',           '2024/25',  40.00,  38.00, '2025-01-28'),
            ('Victor Osimhen',        'Napoli',                'Galatasaray',           '2024/25',  75.00,  70.00, '2024-09-01'),
            ('Federico Chiesa',       'Juventus',              'Liverpool',             '2024/25',  13.00,  12.00, '2024-08-30'),
            ('Mikel Merino',          'Real Sociedad',         'Arsenal',               '2024/25',  32.00,  30.00, '2024-08-23'),
            ('Riccardo Calafiori',    'Bologna',               'Arsenal',               '2024/25',  45.00,  42.00, '2024-07-25'),
            ('David Raya',            'Brentford',             'Arsenal',               '2024/25',  35.00,  33.00, '2024-07-01'),
            ('Joao Pedro',            'Brighton',              'Chelsea',               '2024/25',  30.00,  28.00, '2024-07-01'),
            ('Renato Veiga',          'Basel',                 'Chelsea',               '2024/25',  12.00,  11.00, '2024-07-01'),
            ('Kiernan Dewsbury-Hall', 'Leicester City',        'Chelsea',               '2024/25',  30.00,  28.00, '2024-07-01'),
            ('Omari Kellyman',        'Aston Villa',           'Chelsea',               '2024/25',  24.00,  22.00, '2024-07-01'),
            ('Marc Guiu',             'Barcelona',             'Chelsea',               '2024/25',  12.00,  11.00, '2024-07-01'),
            ('Florian Wirtz',         'Bayer Leverkusen',      'Real Madrid',           '2024/25', 150.00, 145.00, '2025-06-01'),
            ('Trent Alexander-Arnold','Liverpool',             'Real Madrid',           '2024/25',   0.00,   0.00, '2025-07-01'),
            ('Bryan Mbeumo',          'Brentford',             'Manchester United',     '2024/25',  65.00,  62.00, '2025-07-01'),
            ('Matthijs de Ligt',      'Bayern Munich',         'Manchester United',     '2024/25',  45.00,  42.00, '2024-08-13'),
            ('Noussair Mazraoui',     'Bayern Munich',         'Manchester United',     '2024/25',  15.00,  14.00, '2024-08-13'),
            ('Manuel Ugarte',         'Paris Saint-Germain',   'Manchester United',     '2024/25',  50.00,  47.00, '2024-08-29'),

            # ===== NEW 50 TRANSFERS =====

            # 2020/21
            ('Thomas Partey',         'Atletico Madrid',       'Arsenal',               '2020/21',  50.00,  48.00, '2020-10-05'),
            ('Ruben Dias',            'Benfica',               'Manchester City',        '2020/21',  68.00,  65.00, '2020-09-26'),
            ('Kai Havertz',           'Bayer Leverkusen',      'Chelsea',               '2020/21',  80.00,  76.00, '2020-09-04'),
            ('Timo Werner',           'RB Leipzig',            'Chelsea',               '2020/21',  53.00,  50.00, '2020-07-01'),
            ('Hakim Ziyech',          'Ajax',                  'Chelsea',               '2020/21',  40.00,  38.00, '2020-07-01'),
            ('Ben Chilwell',          'Leicester City',        'Chelsea',               '2020/21',  50.00,  47.00, '2020-08-27'),
            ('Thiago Alcantara',      'Bayern Munich',         'Liverpool',             '2020/21',  27.00,  25.00, '2020-09-18'),
            ('Diogo Jota',            'Wolverhampton',         'Liverpool',             '2020/21',  41.00,  39.00, '2020-09-19'),
            ('Donny van de Beek',     'Ajax',                  'Manchester United',     '2020/21',  39.00,  37.00, '2020-09-02'),
            ('Sergio Reguilon',       'Sevilla',               'Tottenham Hotspur',     '2020/21',  30.00,  28.00, '2020-09-17'),

            # 2021/22
            ('Ibrahima Konate',       'RB Leipzig',            'Liverpool',             '2021/22',  40.00,  38.00, '2021-06-01'),
            ('Eduardo Camavinga',     'Rennes',                'Real Madrid',           '2021/22',  31.00,  29.00, '2021-08-31'),
            ('Rodrigo Bentancur',     'Juventus',              'Tottenham Hotspur',     '2021/22',  25.00,  23.00, '2022-01-31'),
            ('Ferran Torres',         'Manchester City',       'Barcelona',             '2021/22',  55.00,  52.00, '2022-01-03'),
            ('Lucas Digne',           'Everton',               'Aston Villa',           '2021/22',  25.00,  23.00, '2022-01-12'),

            # 2022/23
            ('Alexis Mac Allister',   'Brighton',              'Liverpool',             '2022/23',  35.00,  33.00, '2023-06-12'),
            ('Dominik Szoboszlai',    'RB Leipzig',            'Liverpool',             '2022/23',  70.00,  66.00, '2023-07-01'),
            ('Ryan Gravenberch',      'Bayern Munich',         'Liverpool',             '2022/23',  40.00,  38.00, '2023-08-18'),
            ('Lucas Hernandez',       'Bayern Munich',         'Paris Saint-Germain',   '2022/23',  45.00,  42.00, '2023-07-01'),
            ('Milan Skriniar',        'Inter Milan',           'Paris Saint-Germain',   '2022/23',   0.00,   0.00, '2023-07-01'),
            ('Marcus Thuram',         'Borussia Monchengladbach','Inter Milan',         '2022/23',   0.00,   0.00, '2023-07-01'),
            ('Randal Kolo Muani',     'Eintracht Frankfurt',   'Paris Saint-Germain',   '2022/23',  95.00,  90.00, '2023-08-29'),
            ('Manuel Ugarte',         'Sporting CP',           'Paris Saint-Germain',   '2022/23',  60.00,  57.00, '2023-07-12'),
            ('Youri Tielemans',       'Leicester City',        'Aston Villa',           '2022/23',   0.00,   0.00, '2023-07-01'),
            ('Wilfried Gnonto',       'Zurich',                'Leeds United',          '2022/23',   4.00,   3.50, '2022-08-31'),

            # 2023/24
            ('Christopher Nkunku',    'RB Leipzig',            'Chelsea',               '2023/24',  60.00,  57.00, '2023-07-01'),
            ('Axel Disasi',           'Monaco',                'Chelsea',               '2023/24',  45.00,  42.00, '2023-07-14'),
            ('Nicolas Jackson',       'Villarreal',            'Chelsea',               '2023/24',  37.00,  35.00, '2023-06-30'),
            ('Goncalo Ramos',         'Benfica',               'Paris Saint-Germain',   '2023/24',  65.00,  62.00, '2023-08-07'),
            ('Ousmane Dembele',       'Barcelona',             'Paris Saint-Germain',   '2023/24',  50.00,  47.00, '2023-07-01'),
            ('Bradley Barcola',       'Lyon',                  'Paris Saint-Germain',   '2023/24',  45.00,  42.00, '2023-08-01'),
            ('Ivan Toney',            'Brentford',             'Al-Ahli',               '2023/24',  40.00,  38.00, '2024-08-01'),
            ('Lamine Yamal',          'Barcelona',             'Barcelona',             '2023/24',   0.00,   0.00, '2023-07-01'),
            ('Warren Zaire-Emery',    'Paris Saint-Germain',   'Paris Saint-Germain',   '2023/24',   0.00,   0.00, '2023-07-01'),
            ('Virgil van Dijk',       'Liverpool',             'Liverpool',             '2023/24',   0.00,   0.00, '2024-08-01'),

            # 2024/25
            ('Dani Olmo',             'RB Leipzig',            'Barcelona',             '2024/25',  55.00,  52.00, '2024-07-25'),
            ('Desire Doue',           'Rennes',                'Paris Saint-Germain',   '2024/25',  50.00,  48.00, '2024-07-26'),
            ('Khephren Thuram',       'Nice',                  'Juventus',              '2024/25',  25.00,  23.00, '2024-07-01'),
            ('Omar Marmoush',         'Eintracht Frankfurt',   'Manchester City',        '2024/25',  75.00,  72.00, '2025-01-22'),
            ('Abdukodir Khusanov',    'Lens',                  'Manchester City',        '2024/25',  13.00,  12.00, '2025-01-27'),
            ('Vitor Reis',            'Palmeiras',             'Manchester City',        '2024/25',  35.00,  33.00, '2025-01-21'),
            ('Viktor Gyokeres',       'Sporting CP',           'Arsenal',               '2024/25',  75.00,  72.00, '2025-07-01'),
            ('Martin Zubimendi',      'Real Sociedad',         'Liverpool',             '2024/25',  60.00,  58.00, '2024-08-22'),
            ('Federico Valverde',     'Real Madrid',           'Real Madrid',           '2024/25',   0.00,   0.00, '2024-07-01'),
            ('Vinicius Jr',           'Real Madrid',           'Real Madrid',           '2024/25',   0.00,   0.00, '2024-07-01'),
            ('Rodrygo',               'Real Madrid',           'Real Madrid',           '2024/25',   0.00,   0.00, '2024-07-01'),
            ('Jonathan David',        'Lille',                 'Juventus',              '2024/25',   0.00,   0.00, '2025-07-01'),
            ('Rayan Cherki',          'Lyon',                  'Paris Saint-Germain',   '2024/25',  25.00,  23.00, '2025-01-31'),
        ]

        created = 0
        skipped = 0
        errors = 0

        for (player_name, club_from_name, club_to_name, season_name, price, tft_price, date_str) in transfers_data:
            try:
                player = Player.objects.filter(name__iexact=player_name).first()
                club_from = Club.objects.filter(name__iexact=club_from_name).first()
                club_to = Club.objects.filter(name__iexact=club_to_name).first()
                season = seasons.get(season_name)

                if not player:
                    self.stdout.write(self.style.WARNING(f'  Player not found: {player_name}'))
                    skipped += 1
                    continue
                if not club_from:
                    self.stdout.write(self.style.WARNING(f'  Club not found (from): {club_from_name}'))
                    skipped += 1
                    continue
                if not club_to:
                    self.stdout.write(self.style.WARNING(f'  Club not found (to): {club_to_name}'))
                    skipped += 1
                    continue

                transfer, was_created = Transfer.objects.get_or_create(
                    player=player,
                    club_from=club_from,
                    club_to=club_to,
                    season=season,
                    defaults={
                        'price': price,
                        'tft_price': tft_price,
                        'date': parse_date(date_str),
                    }
                )
                if was_created:
                    created += 1
                    self.stdout.write(f'  ✅ {player_name}: {club_from_name} → {club_to_name} ({season_name})')
                else:
                    skipped += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Error on {player_name}: {e}'))
                errors += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created} | Already existed: {skipped} | Errors: {errors}'
        ))
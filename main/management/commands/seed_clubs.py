from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from main.models import Country, Club
import urllib.request
import datetime
import os


CLUBS_DATA = {
    "England": [
        {"name": "Manchester City", "president": "Khaldoon Al Mubarak", "coach": "Pep Guardiola", "found_date": "1880-05-23", "logo_url": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"},
        {"name": "Arsenal", "president": "Stan Kroenke", "coach": "Mikel Arteta", "found_date": "1886-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg"},
        {"name": "Liverpool", "president": "Tom Werner", "coach": "Arne Slot", "found_date": "1892-06-03", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg"},
        {"name": "Chelsea", "president": "Todd Boehly", "coach": "Enzo Maresca", "found_date": "1905-03-10", "logo_url": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg"},
        {"name": "Manchester United", "president": "Jim Ratcliffe", "coach": "Ruben Amorim", "found_date": "1878-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"},
        {"name": "Tottenham Hotspur", "president": "Daniel Levy", "coach": "Ange Postecoglou", "found_date": "1882-09-05", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"},
        {"name": "Newcastle United", "president": "Yasir Al-Rumayyan", "coach": "Eddie Howe", "found_date": "1892-12-09", "logo_url": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg"},
        {"name": "Aston Villa", "president": "Nassef Sawiris", "coach": "Unai Emery", "found_date": "1874-11-21", "logo_url": "https://upload.wikimedia.org/wikipedia/en/9/9f/Aston_Villa_FC_crest_%282016%29.svg"},
        {"name": "West Ham United", "president": "David Sullivan", "coach": "Julen Lopetegui", "found_date": "1895-06-29", "logo_url": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg"},
        {"name": "Brighton", "president": "Tony Bloom", "coach": "Fabian Hurzeler", "found_date": "1901-06-24", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg"},
    ],
    "Spain": [
        {"name": "Real Madrid", "president": "Florentino Pérez", "coach": "Carlo Ancelotti", "found_date": "1902-03-06", "logo_url": "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg"},
        {"name": "Barcelona", "president": "Joan Laporta", "coach": "Hansi Flick", "found_date": "1899-11-29", "logo_url": "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg"},
        {"name": "Atletico Madrid", "president": "Enrique Cerezo", "coach": "Diego Simeone", "found_date": "1903-04-26", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/f4/Atletico_de_madrid_2017_logo.svg"},
        {"name": "Sevilla", "president": "José María del Nido Carrasco", "coach": "Francisco Javier García Pimienta", "found_date": "1890-01-25", "logo_url": "https://upload.wikimedia.org/wikipedia/en/3/3b/Sevilla_FC_logo.svg"},
        {"name": "Real Sociedad", "president": "Jokin Aperribay", "coach": "Imanol Alguacil", "found_date": "1909-09-07", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/f1/Real_Sociedad_logo.svg"},
        {"name": "Villarreal", "president": "Fernando Roig", "coach": "Marcelino García Toral", "found_date": "1923-03-10", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b9/Villarreal_CF_logo.svg"},
        {"name": "Athletic Bilbao", "president": "Jon Uriarte", "coach": "Ernesto Valverde", "found_date": "1898-07-28", "logo_url": "https://upload.wikimedia.org/wikipedia/en/9/98/Club_Athletic_de_Bilbao_logo.svg"},
        {"name": "Real Betis", "president": "Ángel Haro", "coach": "Manuel Pellegrini", "found_date": "1907-09-12", "logo_url": "https://upload.wikimedia.org/wikipedia/en/1/13/Real_betis_logo.svg"},
        {"name": "Valencia", "president": "Layhoon Chan", "coach": "Rubén Baraja", "found_date": "1919-03-05", "logo_url": "https://upload.wikimedia.org/wikipedia/en/c/ce/Valenciacf.svg"},
        {"name": "Osasuna", "president": "Luis Sabalza", "coach": "Jagoba Arrasate", "found_date": "1920-10-24", "logo_url": "https://upload.wikimedia.org/wikipedia/en/d/d5/CA_Osasuna_logo.svg"},
    ],
    "Italy": [
        {"name": "Inter Milan", "president": "Steven Zhang", "coach": "Simone Inzaghi", "found_date": "1908-03-09", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/0/05/FC_Internazionale_Milano_2021.svg"},
        {"name": "AC Milan", "president": "Paolo Scaroni", "coach": "Paulo Fonseca", "found_date": "1899-12-16", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/d/d0/Logo_of_AC_Milan.svg"},
        {"name": "Juventus", "president": "Gianluca Ferrero", "coach": "Thiago Motta", "found_date": "1897-11-01", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/15/Juventus_FC_2017_logo.svg"},
        {"name": "Napoli", "president": "Aurelio De Laurentiis", "coach": "Antonio Conte", "found_date": "1926-08-01", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2d/SSC_Neapel.svg"},
        {"name": "AS Roma", "president": "Dan Friedkin", "coach": "Ivan Juric", "found_date": "1927-06-07", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/f7/AS_Roma_logo_%282017%29.svg"},
        {"name": "Lazio", "president": "Claudio Lotito", "coach": "Marco Baroni", "found_date": "1900-01-09", "logo_url": "https://upload.wikimedia.org/wikipedia/en/7/71/SS_Lazio_Badge.svg"},
        {"name": "Atalanta", "president": "Antonio Percassi", "coach": "Gian Piero Gasperini", "found_date": "1907-10-17", "logo_url": "https://upload.wikimedia.org/wikipedia/en/6/66/AtalantaBC.svg"},
        {"name": "Fiorentina", "president": "Rocco Commisso", "coach": "Raffaele Palladino", "found_date": "1926-08-29", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/e/e4/ACF_Fiorentina_2022.svg"},
        {"name": "Torino", "president": "Urbano Cairo", "coach": "Paolo Vanoli", "found_date": "1906-12-03", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Torino_FC_Logo.svg"},
        {"name": "Bologna", "president": "Joey Saputo", "coach": "Vincenzo Italiano", "found_date": "1909-10-03", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Bologna_F.C._1909_logo.svg"},
    ],
    "Germany": [
        {"name": "Bayern Munich", "president": "Herbert Hainer", "coach": "Vincent Kompany", "found_date": "1900-02-27", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282002%E2%80%932017%29.svg"},
        {"name": "Borussia Dortmund", "president": "Hans-Joachim Watzke", "coach": "Niko Kovač", "found_date": "1909-12-19", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg"},
        {"name": "RB Leipzig", "president": "Oliver Mintzlaff", "coach": "Marco Rose", "found_date": "2009-05-19", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/04/RB_Leipzig_2014_logo.svg"},
        {"name": "Bayer Leverkusen", "president": "Fernando Carro", "coach": "Xabi Alonso", "found_date": "1904-11-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/5/59/Bayer_04_Leverkusen_logo.svg"},
        {"name": "Eintracht Frankfurt", "president": "Mathias Beck", "coach": "Dino Toppmöller", "found_date": "1899-03-08", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/0/04/Eintracht_Frankfurt_Logo.svg"},
        {"name": "Wolfsburg", "president": "Werner Engelhard", "coach": "Ralph Hasenhüttl", "found_date": "1945-09-12", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Logo-VfL-Wolfsburg.svg"},
        {"name": "Borussia Mönchengladbach", "president": "Rolf Königs", "coach": "Gerardo Seoane", "found_date": "1900-08-01", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/8/81/Borussia_M%C3%B6nchengladbach_logo.svg"},
        {"name": "Union Berlin", "president": "Dirk Zingler", "coach": "Bo Svensson", "found_date": "1906-01-17", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/4/44/1._FC_Union_Berlin_Logo.svg"},
        {"name": "Freiburg", "president": "Fritz Keller", "coach": "Julian Schuster", "found_date": "1904-05-30", "logo_url": "https://upload.wikimedia.org/wikipedia/de/f/f7/Logo-sc-freiburg.svg"},
        {"name": "Stuttgart", "president": "Claus Vogt", "coach": "Sebastian Hoeneß", "found_date": "1893-09-09", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/e/eb/VfB_Stuttgart_1893_Logo.svg"},
    ],
    "France": [
        {"name": "Paris Saint-Germain", "president": "Nasser Al-Khelaifi", "coach": "Luis Enrique", "found_date": "1970-08-12", "logo_url": "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg"},
        {"name": "Olympique de Marseille", "president": "Pablo Longoria", "coach": "Roberto De Zerbi", "found_date": "1899-10-26", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Olympique_Marseille_logo.svg"},
        {"name": "Olympique Lyonnais", "president": "John Textor", "coach": "Pierre Sage", "found_date": "1899-10-03", "logo_url": "https://upload.wikimedia.org/wikipedia/en/e/e9/Olympique_Lyonnais.svg"},
        {"name": "Monaco", "president": "Dmitry Rybolovlev", "coach": "Adi Hütter", "found_date": "1924-08-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/e/ea/AS_Monaco_FC.svg"},
        {"name": "Lille", "president": "Olivier Létang", "coach": "Bruno Genesio", "found_date": "1944-10-29", "logo_url": "https://upload.wikimedia.org/wikipedia/en/7/73/LOSC_Lille_logo_%282018%29.svg"},
        {"name": "Lens", "president": "Joseph Oughourlian", "coach": "Will Still", "found_date": "1906-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/6/68/RC_Lens_logo.svg"},
        {"name": "Nice", "president": "Jean-Pierre Rivère", "coach": "Franck Haise", "found_date": "1904-06-26", "logo_url": "https://upload.wikimedia.org/wikipedia/en/2/27/OGC_Nice_logo.svg"},
        {"name": "Rennes", "president": "Nicolas Holveck", "coach": "Jorge Sampaoli", "found_date": "1901-03-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/d/d7/Stade_Rennais_FC.svg"},
        {"name": "Strasbourg", "president": "Marc Keller", "coach": "Liam Rosenior", "found_date": "1906-06-20", "logo_url": "https://upload.wikimedia.org/wikipedia/en/9/99/RC_Strasbourg_Alsace_logo.svg"},
        {"name": "Nantes", "president": "Waldemar Kita", "coach": "Antoine Kombouaré", "found_date": "1943-03-06", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b2/FC_Nantes_logo.svg"},
    ],
    "Portugal": [
        {"name": "Benfica", "president": "Rui Costa", "coach": "Bruno Lage", "found_date": "1904-02-28", "logo_url": "https://upload.wikimedia.org/wikipedia/en/a/a2/SL_Benfica_logo.svg"},
        {"name": "Porto", "president": "André Villas-Boas", "coach": "Vítor Bruno", "found_date": "1893-09-28", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/f4/FC_Porto.svg"},
        {"name": "Sporting CP", "president": "Frederico Varandas", "coach": "Rúben Amorim", "found_date": "1906-07-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/f1/Sporting_CP_logo.svg"},
        {"name": "Braga", "president": "António Salvador", "coach": "Carlos Carvalhal", "found_date": "1921-01-19", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/02/SC_Braga_logo.svg"},
        {"name": "Vitória de Guimarães", "president": "António Miguel Cardoso", "coach": "Rui Borges", "found_date": "1923-10-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/0e/Vitoria_SC_logo.svg"},
        {"name": "Boavista", "president": "Vítor Murta", "coach": "Petit", "found_date": "1903-08-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b6/Boavista_FC_logo.svg"},
        {"name": "Famalicão", "president": "Miguel Ribeiro", "coach": "João Pedro Sousa", "found_date": "1931-01-18", "logo_url": "https://upload.wikimedia.org/wikipedia/en/7/72/FC_Famalic%C3%A3o_logo.svg"},
        {"name": "Gil Vicente", "president": "Francisco Dias da Silva", "coach": "Daniel Sousa", "found_date": "1924-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/4/46/Gil_Vicente_FC_logo.svg"},
        {"name": "Casa Pia", "president": "Pedro Dias", "coach": "Filipe Martins", "found_date": "1920-03-27", "logo_url": "https://upload.wikimedia.org/wikipedia/en/3/36/Casa_Pia_AC.svg"},
        {"name": "Moreirense", "president": "Victor Magalhães", "coach": "Paulo Alves", "found_date": "1938-04-20", "logo_url": "https://upload.wikimedia.org/wikipedia/en/6/60/Moreirense_FC_logo.svg"},
    ],
    "Netherlands": [
        {"name": "Ajax", "president": "Leen Meijaard", "coach": "Francesco Farioli", "found_date": "1900-03-18", "logo_url": "https://upload.wikimedia.org/wikipedia/en/7/79/Ajax_Amsterdam.svg"},
        {"name": "PSV Eindhoven", "president": "Marcel Brands", "coach": "Peter Bosz", "found_date": "1913-08-31", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/05/PSV_Eindhoven.svg"},
        {"name": "Feyenoord", "president": "Tines Rietdijk", "coach": "Brian Priske", "found_date": "1908-07-19", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b3/Feyenoord_logo.svg"},
        {"name": "AZ Alkmaar", "president": "Robert Eenhoorn", "coach": "Maarten Martens", "found_date": "1967-05-18", "logo_url": "https://upload.wikimedia.org/wikipedia/en/4/4f/AZ_Alkmaar.svg"},
        {"name": "Utrecht", "president": "Frans van Seumeren", "coach": "Ron Jans", "found_date": "1970-07-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b9/FC_Utrecht_logo.svg"},
        {"name": "Twente", "president": "Paul van der Kraan", "coach": "Joseph Oosting", "found_date": "1965-07-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/ba/FC_Twente.svg"},
        {"name": "Vitesse", "president": "Coley Parry", "coach": "John van den Brom", "found_date": "1892-05-05", "logo_url": "https://upload.wikimedia.org/wikipedia/en/c/c5/SBV_Vitesse_logo.svg"},
        {"name": "Groningen", "president": "Wouter Gudde", "coach": "Dick Lukkien", "found_date": "1971-01-16", "logo_url": "https://upload.wikimedia.org/wikipedia/en/3/36/FC_Groningen_logo.svg"},
        {"name": "Heerenveen", "president": "Bert Beukema", "coach": "Robin van Persie", "found_date": "1920-07-04", "logo_url": "https://upload.wikimedia.org/wikipedia/en/4/41/SC_Heerenveen_logo.svg"},
        {"name": "Sparta Rotterdam", "president": "Manfred Laros", "coach": "Maurice Steijn", "found_date": "1888-04-03", "logo_url": "https://upload.wikimedia.org/wikipedia/en/3/39/Sparta_Rotterdam.svg"},
    ],
    "Brazil": [
        {"name": "Flamengo", "president": "Rodolfo Landim", "coach": "Filipe Luís", "found_date": "1895-11-15", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Flamengo_braz_06282006.svg"},
        {"name": "Palmeiras", "president": "Leila Pereira", "coach": "Abel Ferreira", "found_date": "1914-08-26", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/10/Palmeiras_logo.svg"},
        {"name": "Corinthians", "president": "Augusto Melo", "coach": "Ramón Díaz", "found_date": "1910-09-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/a/a0/Sport_Club_Corinthians_Paulista_crest.svg"},
        {"name": "São Paulo", "president": "Julio Casares", "coach": "Luis Zubeldía", "found_date": "1930-01-25", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Escudo_do_S%C3%A3o_Paulo_Futebol_Clube.svg"},
        {"name": "Santos", "president": "Marcelo Teixeira", "coach": "Fábio Carille", "found_date": "1912-04-14", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/15/Santos_futebol_clube_escudo.svg"},
        {"name": "Fluminense", "president": "Mário Bittencourt", "coach": "Mano Menezes", "found_date": "1902-07-21", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Fluminense_fc_logo.svg"},
        {"name": "Grêmio", "president": "Alberto Guerra", "coach": "Renato Portaluppi", "found_date": "1903-09-15", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/f1/Gr%C3%AAmio_Foot-Ball_Porto_Alegrense_logo.svg"},
        {"name": "Internacional", "president": "Alessandro Barcellos", "coach": "Roger Machado", "found_date": "1909-04-04", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Escudo_do_Sport_Club_Internacional.svg"},
        {"name": "Atletico Mineiro", "president": "Sérgio Coelho", "coach": "Gabriel Milito", "found_date": "1908-03-25", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Atletico_mineiro_galo.svg"},
        {"name": "Vasco da Gama", "president": "Pedrinho", "coach": "Rafael Paiva", "found_date": "1898-08-21", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/6/60/Club_de_Regatas_Vasco_da_Gama_logo.svg"},
    ],
    "Ukraine": [
        {"name": "Shakhtar Donetsk", "president": "Rinat Akhmetov", "coach": "Marino Pušić", "found_date": "1936-05-24", "logo_url": "https://upload.wikimedia.org/wikipedia/en/a/a0/FC_Shakhtar_Donetsk.svg"},
        {"name": "Dynamo Kyiv", "president": "Ihor Surkis", "coach": "Oleksandr Shovkovskyi", "found_date": "1927-05-13", "logo_url": "https://upload.wikimedia.org/wikipedia/en/9/9d/FC_Dynamo_Kyiv_logo.svg"},
        {"name": "Metalist Kharkiv", "president": "Serhiy Yaroslavsky", "coach": "Oleksandr Huoba", "found_date": "1925-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b5/Metalist_Kharkiv_logo.svg"},
        {"name": "Dnipro-1", "president": "Ihor Kolomoyskyi", "coach": "Oleksiy Drozdov", "found_date": "2017-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/4/4b/SC_Dnipro-1_logo.svg"},
        {"name": "Vorskla Poltava", "president": "Oleksandr Hrabovskyy", "coach": "Yuriy Maksymov", "found_date": "1955-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/e/e7/FC_Vorskla_Poltava_Logo.svg"},
        {"name": "Chornomorets Odessa", "president": "Leonid Klimov", "coach": "Serhiy Shishchenko", "found_date": "1936-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/ba/FC_Chornomorets_Odesa_Logo.svg"},
        {"name": "Desna Chernihiv", "president": "Serhiy Tulub", "coach": "Oleh Hryshchenko", "found_date": "1960-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/6/65/FC_Desna_Chernihiv_Logo.svg"},
        {"name": "Rukh Lviv", "president": "Ihor Didenko", "coach": "Yuriy Hryshchuk", "found_date": "2020-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/c/c4/FC_Rukh_Lviv_logo.svg"},
        {"name": "Minai", "president": "Vasyl Mykolayenko", "coach": "Oleksandr Hlyvynskyy", "found_date": "1977-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/5/50/FC_Mynai_logo.svg"},
        {"name": "Kolos Kovalivka", "president": "Denys Prutko", "coach": "Volodymyr Shelikhov", "found_date": "1925-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/e/e7/FC_Kolos_Kovalivka_logo.svg"},
    ],
    "Russia": [
        {"name": "Zenit St. Petersburg", "president": "Alexander Medvedev", "coach": "Sergei Semak", "found_date": "1925-06-25", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/00/FC_Zenit_Saint_Petersburg_logo.svg"},
        {"name": "CSKA Moscow", "president": "Evgeny Giner", "coach": "Vladimir Fedotov", "found_date": "1911-09-07", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/f8/PFC_CSKA_Moscow_logo.svg"},
        {"name": "Spartak Moscow", "president": "Leonid Fedun", "coach": "Guillermo Abascal", "found_date": "1922-04-18", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/0f/FC_Spartak_Moscow_logo.svg"},
        {"name": "Lokomotiv Moscow", "president": "Ilya Gerkus", "coach": "Mikhail Galaktionov", "found_date": "1922-07-25", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/09/FC_Lokomotiv_Moscow_logo.svg"},
        {"name": "Dynamo Moscow", "president": "Pavel Pivovarov", "coach": "Andy Neville", "found_date": "1923-04-18", "logo_url": "https://upload.wikimedia.org/wikipedia/en/a/ad/FC_Dynamo_Moscow_logo.svg"},
        {"name": "Krasnodar", "president": "Sergei Galitsky", "coach": "Vladislav Nikolaev", "found_date": "2008-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/0f/FC_Krasnodar_logo.svg"},
        {"name": "Rubin Kazan", "president": "Rustam Minnikhanov", "coach": "Leonid Slutsky", "found_date": "1958-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/a/a1/FC_Rubin_Kazan_logo.svg"},
        {"name": "Akhmat Grozny", "president": "Ramzan Kadyrov", "coach": "Aitor Cantalapiedra", "found_date": "1946-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/bf/FC_Akhmat_Grozny_Logo.svg"},
        {"name": "Rostov", "president": "Artur Atoev", "coach": "Valery Karpin", "found_date": "1930-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/8/8e/FC_Rostov_logo.svg"},
        {"name": "Sochi", "president": "Boris Rotenberg", "coach": "Dmitri Gunko", "found_date": "2018-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/8/8d/FC_Sochi_logo.svg"},
    ],
    "Argentina": [
        {"name": "River Plate", "president": "Jorge Brito", "coach": "Marcelo Gallardo", "found_date": "1901-05-25", "logo_url": "https://upload.wikimedia.org/wikipedia/en/b/b3/River_plate_logo_2.svg"},
        {"name": "Boca Juniors", "president": "Juan Román Riquelme", "coach": "Fernando Gago", "found_date": "1905-04-03", "logo_url": "https://upload.wikimedia.org/wikipedia/en/f/f8/Boca_Juniors_logo.svg"},
        {"name": "Racing Club", "president": "Víctor Blanco", "coach": "Gustavo Costas", "found_date": "1903-03-25", "logo_url": "https://upload.wikimedia.org/wikipedia/en/3/31/Racing_Club_logo.svg"},
        {"name": "Independiente", "president": "Hugo Moyano", "coach": "Julio Falcioni", "found_date": "1905-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/07/Independiente_logo.svg"},
        {"name": "San Lorenzo", "president": "Marcelo Moretti", "coach": "Miguel Ángel Russo", "found_date": "1908-04-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/07/San_Lorenzo_de_Almagro_logo.svg"},
        {"name": "Estudiantes", "president": "Juan Sebastián Verón", "coach": "Eduardo Domínguez", "found_date": "1905-08-04", "logo_url": "https://upload.wikimedia.org/wikipedia/en/7/70/Estudiantes_de_La_Plata_logo.svg"},
        {"name": "Vélez Sársfield", "president": "Fabián Berlanga", "coach": "Mauricio Pellegrino", "found_date": "1910-01-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/6/6c/Velez_Sarsfield_logo.svg"},
        {"name": "Huracán", "president": "Lucas Longo", "coach": "Frank Darío Kudelka", "found_date": "1908-11-01", "logo_url": "https://upload.wikimedia.org/wikipedia/en/c/cb/CA_Hur%C3%A1can_logo.svg"},
        {"name": "Lanus", "president": "Nicolás Russo", "coach": "Ricardo Zielinski", "found_date": "1915-01-03", "logo_url": "https://upload.wikimedia.org/wikipedia/en/3/3c/Club_Atletico_Lanus_logo.svg"},
        {"name": "Talleres", "president": "Andrés Fassi", "coach": "Alexander Medina", "found_date": "1913-05-05", "logo_url": "https://upload.wikimedia.org/wikipedia/en/9/90/Talleres_de_C%C3%B3rdoba_logo.svg"},
    ],
}


class Command(BaseCommand):
    help = 'Seed database with top 10 football clubs per country'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing clubs before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing clubs...')
            Club.objects.all().delete()
            self.stdout.write(self.style.WARNING('All clubs deleted.'))

        total_created = 0
        total_skipped = 0

        for country_name, clubs in CLUBS_DATA.items():
            country, _ = Country.objects.get_or_create(name=country_name)
            self.stdout.write(f'\n📍 Processing {country_name}...')

            for club_data in clubs:
                if Club.objects.filter(name=club_data['name']).exists():
                    self.stdout.write(f'  ⏩ Skipped (already exists): {club_data["name"]}')
                    total_skipped += 1
                    continue

                try:
                    found_date = datetime.date.fromisoformat(club_data['found_date'])

                    # Download logo
                    logo_content = None
                    logo_name = None
                    try:
                        req = urllib.request.Request(
                            club_data['logo_url'],
                            headers={'User-Agent': 'Mozilla/5.0'}
                        )
                        with urllib.request.urlopen(req, timeout=10) as response:
                            logo_content = response.read()
                        ext = os.path.splitext(club_data['logo_url'])[1] or '.svg'
                        logo_name = f"{club_data['name'].replace(' ', '_')}{ext}"
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'  ⚠️  Could not download logo for {club_data["name"]}: {e}'))

                    club = Club(
                        country=country,
                        name=club_data['name'],
                        president=club_data['president'],
                        coach=club_data['coach'],
                        found_date=found_date,
                    )

                    if logo_content and logo_name:
                        club.logo.save(logo_name, ContentFile(logo_content), save=False)

                    club.save()
                    self.stdout.write(self.style.SUCCESS(f'  ✅ Created: {club_data["name"]}'))
                    total_created += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ❌ Failed: {club_data["name"]} — {e}'))

        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✅ Done! Created: {total_created} clubs'))
        if total_skipped:
            self.stdout.write(self.style.WARNING(f'⏩ Skipped: {total_skipped} clubs (already existed)'))
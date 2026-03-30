from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum, Avg
from .models import *


def index_view(request):
    countries = Country.objects.all()
    context = {
        'countries': countries,
    }
    return render(request, 'index.html', context)


def clubs_by_country(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    countries = Country.objects.all()
    clubs = Club.objects.filter(country=country)
    context = {
        'country': country,
        'clubs': clubs,
        'countries': countries,
    }
    return render(request, 'country_clubs.html', context)


def clubs_view(request):
    clubs = Club.objects.all()
    countries = Country.objects.all()
    context = {
        'clubs': clubs,
        'countries': countries,
    }
    return render(request, 'clubs.html', context)


def club_details_view(request, id):
    club = get_object_or_404(Club, id=id)
    players = Player.objects.filter(club=club)
    countries = Country.objects.all()
    context = {
        'club': club,
        'players': players,
        'countries': countries,
    }
    return render(request, 'club-details.html', context)


def latest_transfers_view(request):
    transfers = Transfer.objects.all()
    countries = Country.objects.all()
    context = {
        'transfers': transfers,
        'countries': countries,
    }
    return render(request, 'latest-transfers.html', context)


def players_view(request):
    players = Player.objects.all().order_by('-price')
    countries = Country.objects.all()
    context = {
        'players': players,
        'countries': countries,
    }
    return render(request, 'players.html', context)


def u20_payers_view(request):
    u20_players = Player.filtered.all()
    countries = Country.objects.all()
    context = {
        'u20_players': u20_players,
        'countries': countries,
    }
    return render(request, 'U-20-players.html', context)


def tryouts_view(request):
    countries = Country.objects.all()
    context = {
        'countries': countries,
    }
    return render(request, 'tryouts.html', context)


def stats_view(request):
    countries = Country.objects.all()
    context = {
        'countries': countries,
    }
    return render(request, 'stats.html', context)


def about_view(request):
    countries = Country.objects.all()
    context = {
        'countries': countries,
    }
    return render(request, 'about.html', context)

from django.shortcuts import render
from main.models import *
from django.db.models import F
from django.db.models import Sum


def Top150AccuratePredictionsView(request):
    players = Player.objects.all()
    countries = Country.objects.all()
    acc_predicted_players = Player.objects.all().filter(transfers__price=F('transfers__tft_price')).distinct()[:150]
    context = {'acc_pred_players': acc_predicted_players,
               "players": players,
               'countries': countries}
    return render(request, 'stats/150-accurate-predictions.html', context)


def TransfersRecordsView(request):
    countries = Country.objects.all()
    top_transfers = Transfer.objects.order_by('-price')[:50]
    context = {'top_transfers': top_transfers, 'countries': countries}
    return render(request, 'stats/transfer-records.html', context)


def Top50byExpenditure(request):
    countries = Country.objects.all()
    clubs = Club.objects.filter(
        transfers_in__season__name='2022/23').annotate(
        total_spent=Sum('transfers_in__price')).order_by('-total_spent')[:50]

    context = {'clubs': clubs,
               'countries': countries}
    return render(request, "stats/top-50-clubs-by-expenditure.html", context)


def Top50byIncome(request):
    countries = Country.objects.all()
    clubs = Club.objects.filter(
        transfers_in__season__name='2022/23').annotate(
        total_income=Sum('transfers_out__price')).order_by('-total_income')[:50]

    context = {'clubs': clubs,
               'countries': countries}
    return render(request, "stats/top-50-clubs-by-income.html", context)

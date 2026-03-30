from django.contrib import admin
from .models import *


@admin.register(Season)
class SeasonModel(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    list_display_links = ('name', )


@admin.register(Country)
class SeasonModel(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    list_display_links = ('name', )


@admin.register(Club)
class ClubModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'president', 'coach', 'found_date', 'country__name')
    list_display_links = ('name', 'president', 'coach', 'found_date')
    search_fields = ('name', 'coach')
    list_per_page = 10


@admin.register(Player)
class PlayerModel(admin.ModelAdmin):
    list_display = ('name', 'age', 'position', 'number', 'price')
    list_display_links = ('name', 'age', 'position', 'number', 'price')
    search_fields = ('country__name', 'club__name')


@admin.register(Transfer)
class TransferModel(admin.ModelAdmin):
    list_display = ('id', 'club_from', 'club_to', 'price', 'date',)
    list_display_links = ('club_from', 'club_to', 'price', 'date',)
    search_fields = ('club_from', 'club_to', 'price', 'date',)




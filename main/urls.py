from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('clubs/', clubs_view, name='clubs'),
    path('clubs/<int:country_id>/', clubs_by_country, name='clubs_by_country'),
    path('clubs/details/<int:id>/', club_details_view, name='club_details'),
    path('latest-transfers/', latest_transfers_view, name='latest-transfers'),
    path('players/', players_view, name='players'),
    path('u20-players/', u20_payers_view, name='u20-players'),
    path('tryouts/', tryouts_view, name='tryouts'),
    path('stats/', stats_view, name='stats'),
    path('about/', about_view, name='about'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

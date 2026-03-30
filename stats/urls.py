from django.urls import path
from .views import Top150AccuratePredictionsView, TransfersRecordsView, Top50byExpenditure, Top50byIncome

urlpatterns = [
    path('top150/', Top150AccuratePredictionsView, name='top150'),
    path('transfer-records/', TransfersRecordsView, name='transfer_records'),
    path('top50-by-expenditure/', Top50byExpenditure, name='expenditure'),
    path('top50-by-income/', Top50byIncome, name='income'),
]

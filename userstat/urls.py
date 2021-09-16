from .views import ExpensesSummaryStats, IncomeSummaryStats
from django.urls import path

urlpatterns = [
    path('expense-category-data', ExpensesSummaryStats.as_view(), name='expense-category-data'),
    path('income-source-data', IncomeSummaryStats.as_view(), name='income-source-data'),
]



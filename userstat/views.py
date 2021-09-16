from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status, response

from expenses.models import Expenses
from income.models import Income

import datetime

class ExpensesSummaryStats(APIView):

    # calculate amount for category
    def get_amount_for_category(self, expenses_list, category):
        expenses = expenses_list.filter(category=category)

        amount=0
        for expense in expenses:
            amount +=expense.amount

        return {'amount': str(amount)}

    # to get categories
    def get_category(self, expense):
        return expense.category
    
    def get(self, request):
        today_date = datetime.date.today()
        ayear_ago = today_date-datetime.timedelta(days=12*30)

        expenses = Expenses.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=today_date)
        final={}
        # map to map category, set to remove duplications, and list to have the data only
        categories = list(set(map(self.get_category, expenses)))

        for category in categories:
            final[category] = self.get_amount_for_category(expenses, category)

        return response.Response({"category_data":final}, status=status.HTTP_200_OK)

class IncomeSummaryStats(APIView):

    # calculate amount for income source
    def get_amount_for_source(self, income_list, source):
        income = income_list.filter(source=source)

        amount=0
        for i in income:
            amount +=i.amount

        return {'amount': str(amount)}

    # to get income sources
    def get_income_sources(self, income):
        return income.source
    
    def get(self, request):
        today_date = datetime.date.today()
        ayear_ago = today_date-datetime.timedelta(days=12*30)

        income = Income.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=today_date)
        final={}
        # map to map category, set to remove duplications, and list to have the data only
        sources = list(set(map(self.get_income_sources, income)))

        for source in sources:
            final[source] = self.get_amount_for_source(income, source)

        return response.Response({"income_soruces_data":final}, status=status.HTTP_200_OK)





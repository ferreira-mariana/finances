from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

from .models import AccountEntry

import datetime

def index(request):
    latest_entry_list = AccountEntry.objects.order_by('-date')[:5]
    latest_expense_list = AccountEntry.objects.filter(entry_type='out')[:5]
    latest_income_list = AccountEntry.objects.filter(entry_type='in')[:5]
    context = {
        'latest_entry_list': latest_entry_list,
        'latest_expense_list': latest_expense_list,
        'latest_income_list': latest_income_list,
    }
    return render(request, 'finances/index.html', context)

def detail(request, entry_id):
    entry = get_object_or_404(AccountEntry, pk=entry_id)
    return render(request, 'finances/detail.html', {'entry': entry})

def month(request, year, month):    
    expense_list = get_list_or_404(AccountEntry, date__year=year, date__month=month, entry_type='out')
    income_list = get_list_or_404(AccountEntry, date__year=year, date__month=month, entry_type='in')
    total_expense = sum(e.amount for e in expense_list)
    total_income = sum(i.amount for i in income_list)
    savings = total_income - total_expense
    month_name = datetime.date(year, month, 1).strftime("%B")
    context = {
        'month_expenses': expense_list,
        'month_incomes': income_list,
        'total_expense': total_expense,
        'total_income': total_income,
        'savings': savings,
        'year': year,
        'month': month_name,
    }
    return render(request, 'finances/month.html', context)
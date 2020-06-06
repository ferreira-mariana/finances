from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

from .models import AccountEntry

import datetime

def index(request):
    latest_entry_list = AccountEntry.objects.order_by('-date')[:5]
    latest_expense_list = AccountEntry.objects.filter(entry_type='out')
    latest_income_list = AccountEntry.objects.filter(entry_type='in')
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
    entry_list = get_list_or_404(AccountEntry, date__year=year, date__month=month)
    month_name = datetime.date(year, month, 1).strftime("%B")
    context = {
        'month_entries': entry_list,
        'year': year,
        'month': month_name,
    }
    return render(request, 'finances/month.html', context)
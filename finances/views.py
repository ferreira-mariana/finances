from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import AccountEntry

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
    d = '{}/{}'.format(year,month)
    return HttpResponse("You're looking at month %s." % d)
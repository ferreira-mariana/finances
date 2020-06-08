from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404

from .models import AccountEntry
from .forms import AddNewEntry

import datetime

def index(request):
    latest_entry_list = AccountEntry.objects.order_by('-date')[:5]
    latest_expense_list = AccountEntry.objects.filter(entry_type='out')[:5]
    latest_income_list = AccountEntry.objects.filter(entry_type='in')[:5]
    date = datetime.date.today()

    if request.method == 'POST':
        entry_added = get_object_or_404(AccountEntry.objects.order_by('-id')[:1])
    else:
        entry_added = ''

    context = {
        'latest_entry_list': latest_entry_list,
        'latest_expense_list': latest_expense_list,
        'latest_income_list': latest_income_list,
        'entry_added': entry_added,
        'current_year': date.year,
        'current_month': date.month,
    }
    return render(request, 'finances/index.html', context)

def detail(request, entry_id):
    entry = get_object_or_404(AccountEntry, pk=entry_id)
    return render(request, 'finances/detail.html', {'entry': entry})

def month(request, year, month):    
    expense_list = get_list_or_404(AccountEntry.objects.order_by('-date'), date__year=year, date__month=month, entry_type='out')
    income_list = get_list_or_404(AccountEntry.objects.order_by('-date'), date__year=year, date__month=month, entry_type='in')
    total_expense = sum(e.amount for e in expense_list)
    total_income = sum(i.amount for i in income_list)
    savings = total_income - total_expense

    #data for charts
    labels = ['income', 'expense']
    data = [total_income, total_expense]

    categories_names = []
    for e in expense_list: 
        categories_names.append(e.category)
    categories_amount = []
    for name in categories_names:
        amount = sum(e.amount for e in expense_list if e.category == name)
        categories_amount.append(amount)
    categories_dict = {categories_names[i]: categories_amount[i] for i in range(len(categories_names))}
    
    month_name = datetime.date(year, month, 1).strftime("%B")
    context = {
        'month_expenses': expense_list,
        'month_incomes': income_list,
        'total_expense': total_expense,
        'total_income': total_income,
        'savings': savings,
        'categories_dict': categories_dict,
        'year': year,
        'month': month_name,
        'labels': labels,
        'data': data,
    }
    return render(request, 'finances/month.html', context)

def new_entry(request):
    if request.method == 'POST':
        form = AddNewEntry(request.POST)
        if form.is_valid():
            entry = AccountEntry(
                name = request.POST['name'],
                amount = request.POST['amount'],
                category = request.POST['category'],
                date = request.POST['date'],
                entry_type = request.POST['entry_type'],
            )
            entry.save()
            return index(request)
    else:
        form = AddNewEntry()

    return render(request, 'finances/new_entry.html', {'form': form})

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import AccountEntry
from .forms import AddNewEntry

import datetime

def get_previous_month(year, month):
    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year
    return {'previous_year': previous_year, 'previous_month': previous_month}

def get_month_context(request, year, month):
    expense_list = AccountEntry.objects.order_by('-date').filter(date__year=year, date__month=month, entry_type='out')
    income_list = AccountEntry.objects.order_by('-date').filter(date__year=year, date__month=month, entry_type='in')
    total_expense = sum(e.amount for e in expense_list)
    total_income = sum(i.amount for i in income_list)
    savings = round( total_income - total_expense, 2 )

    #data for charts
    if savings > 0:
        labels = ['income', 'expense', 'savings']
        data = [total_income, total_expense, savings]
        savings_message = 'You saved R$ {}! :D '.format(savings)
    else:
        labels = ['income', 'expense']
        data = [total_income, total_expense]
        if savings == 0:
            savings_message = 'You spent exactly what you earned.'
        else:
            savings_message = 'You spent more R$ {} than you earned :('.format(-savings)

    categories_names = []
    for e in expense_list: 
        if not (e.category in categories_names):
            categories_names.append(e.category)
    categories_amount = []
    colors = ["#8e5ea2", "#FFB946","#3e95cd","#F7685B", "#3cba9f"] #colors for bar chart
    background_colors = []
    for index, name in enumerate(categories_names):
        amount = sum(e.amount for e in expense_list if e.category == name)
        categories_amount.append(amount)
        background_colors.append(colors[index % len(colors)]) 
    categories_dict = {categories_names[i]: categories_amount[i] for i in range(len(categories_names))}

    month_name = datetime.date(year, month, 1).strftime("%B")
    context = {
        'month_expenses': expense_list,
        'month_incomes': income_list,
        'total_expense': total_expense,
        'total_income': total_income,
        'savings': savings,
        'categories_dict': categories_dict,
        'categories_names': categories_names,
        'categories_amount': categories_amount,
        'background_colors': background_colors,
        'year': year,
        'month': month_name,
        'labels': labels,
        'data': data,
        'savings_message': savings_message,
    }
    return context

def index(request):
    date = datetime.date.today()

    context = {
        'current_year': date.year,
        'current_month': date.month,
    }
    month_context = get_month_context(request, date.year, date.month)
    previous_month = get_previous_month(date.year, date.month)
    context = {**context, **month_context, **previous_month}
    return render(request, 'finances/index.html', context)

def month(request, year, month):    
    context = get_month_context(request, year, month)
    return render(request, 'finances/month.html', context)

def new_entry(request):
    if request.method == 'POST':
        form = AddNewEntry(request.POST)
        if form.is_valid():
            entry = AccountEntry(
                name = request.POST['name'],
                amount = request.POST['amount'],
                category = request.POST['category'].capitalize(),
                date = request.POST['date'],
                entry_type = request.POST['entry_type'],
            )
            entry.save()
            return render(request, 'finances/new_entry.html', {'entry_added': entry})
    else:
        form = AddNewEntry()

    return render(request, 'finances/new_entry.html', {'form': form, "entry_added": ""})

from django.shortcuts import render, redirect
from .models import Income, Source
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

# Create your views here.
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        
        income = Income.objects.filter(
            amount__istartswith=search_str, owner = request.user
        ) | Income.objects.filter(
            date__istartswith=search_str, owner = request.user
        ) | Income.objects.filter(
            description__icontains=search_str, owner = request.user
        ) | Income.objects.filter(
            source__icontains=search_str, owner = request.user
        )
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="/authentication/login")
def index(request):    
    # retrieve the income
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    currency = UserPreference.objects.get(user=request.user).currency
    
    context = {
        'income': income, 
        'page_obj': page_obj,
        'currency': currency
        }
    
    return render(request, 'income/index.html', context)

@login_required(login_url="/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    
    if request.method == 'GET':
        return render(request, 'income/add_income.html',context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html',context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html',context)
        
        Income.objects.create(amount=amount, description=description, date=date, source=source, owner=request.user)
      
        messages.success(request, 'Added income successfully!')
        
        return redirect('income')
    


@login_required(login_url="/authentication/login")
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    
    context = {
        'income' : income, 
        'values': income,
        'categories': sources
    }
    
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    
    if request.method == 'POST':
        
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html',context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html',context)
        
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        
        income.save()
        
        messages.success(request, 'Updated income successfully!')
        return redirect('income')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Deleted income successfully')
    return redirect('income')
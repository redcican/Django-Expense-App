import datetime
from expenses.models import Category, Expense
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner = request.user
        ) | Expense.objects.filter(
            date__istartswith=search_str, owner = request.user
        ) | Expense.objects.filter(
            description__icontains=search_str, owner = request.user
        ) | Expense.objects.filter(
            category__icontains=search_str, owner = request.user
        )
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url="/authentication/login")
def index(request):
    # categories = Category.objects.all()
    
    # retrieve the expense
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    exists = UserPreference.objects.filter(user=request.user).exists()
    if exists:
        currency = UserPreference.objects.get(user=request.user).currency
    else:
        currency = "USD"
    context = {
        'expenses': expenses, 
        'page_obj': page_obj,
        'currency': currency
        }
    
    return render(request, 'expenses/index.html', context)

@login_required(login_url="/authentication/login")
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST}
    
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html',context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html',context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html',context)
        
        Expense.objects.create(amount=amount, description=description, date=date, category=category,owner=request.user)
      
        messages.success(request, 'Added expense successfully!')
        
        return redirect('expenses')

@login_required(login_url="/authentication/login")
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    
    context = {
        'expense' : expense, 
        'values': expense,
        'categories': categories
    }
    
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    
    if request.method == 'POST':
        
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html',context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html',context)
        
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        
        expense.save()
        
        messages.success(request, 'Updated expense successfully!')
        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Deleted expense successfully')
    return redirect('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
        date__gte = six_months_ago, date__lte = todays_date
    )
    
    finalrep = {}
    
    category_list = list(set([expense.category for expense in expenses]))
    
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
            
        return amount
    
    # for x in expenses:
    for y in category_list:
        finalrep[y] = get_expense_category_amount(y)
                
    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')
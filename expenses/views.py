from expenses.models import Category, Expense
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

@login_required(login_url="/authentication/login")
def index(request):
    # categories = Category.objects.all()
    
    # retrieve the expense
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'expenses': expenses, 'page_obj': page_obj}
    
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
        
        Expense.objects.create(amount=amount, description=description, date=date, category=category,
                               owner=request.user)
      
        messages.success(request, 'Added expense successfully!')
        
        return redirect('expenses')
    
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
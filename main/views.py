from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expenses, Accounts, Incomes, Credits, ShoppingList, Plan
from .forms import ExpensesForm, IncomesForm, AccountsForm, TransferMoneyForm, NewCreditForm, NewShoppingListForm
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime as dt
import datetime

login_url = '/zaloguj'


# Create your views here.

def login_view(request):
    return render(request, 'login.html', {})


def do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/login')


def do_logout(request):
    logout(request)
    return redirect('/zaloguj')


@login_required(login_url=login_url)
def home(request):
    accounts = Accounts.objects.all()[:3]
    credits = Credits.objects.all()[:3]
    shopping_list = ShoppingList.objects.all()[:3]
    data = {
        'current_year': dt.now().year,
        'current_month': dt.now().month,
        'shopping_list': shopping_list,
        'accaunts': accounts,
        'credits': credits,
    }
    return render(request, 'home.html', data)


@login_required(login_url=login_url)
def expenses_view(request):
    if 'year' in request.GET and 'month' in request.GET:
        picked_year = int(request.GET['year'])
        picked_month = int(request.GET['month'])
    else:
        picked_year = dt.now().year
        picked_month = dt.now().month

    expenses = Expenses.objects.filter(purchase_date__year=picked_year, purchase_date__month=picked_month)
    try:
        plan = Plan.objects.all().get(month=picked_month, year=picked_year)
    except ObjectDoesNotExist:
        plan = None


    expenses_sum = {
        'Jedzenie': 0.0,
        'Chemia': 0.0,
        'Kosmetyki_Higiena_Leki': 0.0,
        'Dom': 0.0,
        'Transport': 0.0,
        'Inne': 0.0
    }

    for expense in expenses:
        expenses_sum[expense.category] += expense.total_price

    if plan:
        plan_present = True
        plan_evaluation = {
            'Jedzenie': (plan.jedzenie/100.0) * plan.predicted_income,
            'Chemia': (plan.chemia/100.0) * plan.predicted_income,
            'Kosmetyki_Higiena_Leki': (plan.kosmetyki/100.0) * plan.predicted_income,
            'Dom': (plan.dom/100.0) * plan.predicted_income,
            'Transport': (plan.transport/100.0) * plan.predicted_income,
            'Inne': (plan.inne/100.0) * plan.predicted_income
        }
        used_plan = {
            'Jedzenie': expenses_sum['Jedzenie']/plan_evaluation['Jedzenie']*100,
            'Chemia': expenses_sum['Chemia']/plan_evaluation['Chemia']*100,
            'Kosmetyki_Higiena_Leki': expenses_sum['Kosmetyki_Higiena_Leki']/plan_evaluation['Kosmetyki_Higiena_Leki']*100,
            'Dom': expenses_sum['Dom']/plan_evaluation['Dom']*100,
            'Transport': expenses_sum['Transport']/plan_evaluation['Transport']*100,
            'Inne': expenses_sum['Inne']/plan_evaluation['Inne']*100
        }
    else:
        plan_present = False
        plan_evaluation = None
        used_plan = None

    data = {
        'current_year': dt.now().year,
        'current_month': dt.now().month,
        'picked_year': picked_year,
        'picked_month': picked_month,
        'expenses_list': {
            'Jedzenie': expenses.filter(category='Jedzenie'),
            'Chemia': expenses.filter(category='Chemia'),
            'Kosmetyki_Higiena_Leki': expenses.filter(category='Kosmetyki_Higiena_Leki'),
            'Dom': expenses.filter(category='Dom'),
            'Transport': expenses.filter(category='Transport'),
            'Inne': expenses.filter(category='Inne')
        },
        'expenses_sum': expenses_sum,
        'form': {
            'current_year': dt.now().year,
            'current_month': dt.now().month,
            'form': ExpensesForm()
        },
        'plan_present': plan_present,
        'plan_evaluation': plan_evaluation,
        'used_plan': used_plan,
    }

    return render(request, 'expenses.html', data)


@login_required(login_url=login_url)
def add_expense(request):
    data = {
        'current_year': dt.now().year,
        'current_month': dt.now().month,
        'form': ExpensesForm()
    }
    return render(request, 'add_expense.html', data)


@login_required(login_url=login_url)
def do_add_expense(request):
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            expense = Expenses()
            expense.name = clean_data['name']
            expense.category = clean_data['category']
            expense.quantity = clean_data['quantity']
            expense.unit_price = clean_data['unit_price']
            expense.currency = clean_data['currency']
            expense.unit_name = clean_data['unit_name']
            expense.total_price = clean_data['unit_price'] * clean_data['quantity']
            expense.charged_account = clean_data['charged_account']

            expense.add_expense()

    date = dt.now()

    url = f'/wydatki?year={date.today().year}&month={str(date.today().month)}'
    return redirect(url)


@login_required(login_url=login_url)
def delete_expense(request):
    if request.method == 'POST':
        expense = Expenses.objects.get(id=request.POST['id'])
        expense.delete()
    return redirect('/wydatki')


@login_required(login_url=login_url)
def incomes_view(request):
    if 'year' in request.GET and 'month' in request.GET:
        picked_year = int(request.GET['year'])
        picked_month = int(request.GET['month'])
    else:
        picked_year = dt.now().year
        picked_month = dt.now().month

    incomes = []
    accounts = Accounts.objects.all()

    for account in accounts:
        income = {}
        income['account_name'] = account.accountName
        income['amount'] = account.amount
        income['currency'] = account.currency
        income['incomes'] = Incomes.objects.filter(topped_up_account=account, date__year=picked_year,
                                                   date__month=picked_month).reverse()
        incomes.append(income)

    data = {
        'current_year': dt.now().year,
        'current_month': dt.now().month,
        'picked_year': picked_year,
        'picked_month': picked_month,
        'accounts': incomes,
        'form': IncomesForm(),
        'add_account_form': AccountsForm(),
        'transfer_form': TransferMoneyForm(),
    }
    return render(request, 'incomes.html', data)


@login_required(login_url=login_url)
def do_add_income(request):
    if request.method == 'POST':
        form = IncomesForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            income = Incomes()
            income.name = clean_data['name']
            income.income = clean_data['income']
            income.is_cyclic = False
            income.topped_up_account = clean_data['topped_up_account']
            income.add_income()
    return redirect('/zarobki')


@login_required(login_url=login_url)
def delete_income(request):
    if request.method == 'POST':
        income = Incomes.objects.get(id=request.POST['id'])
        income.delete()
    return redirect('/zarobki')


@login_required(login_url=login_url)
def add_account_e(request):
    if request.method == 'POST':
        form = AccountsForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            account = Accounts()
            account.accountName = clean_data['accountName']
            account.accountType = clean_data['accountType']
            account.amount = clean_data['amount']
            account.currency = clean_data['currency']
            account.is_default = False
            account.add_account()
    return redirect('/zarobki')


@login_required(login_url=login_url)
def transfer_money_e(request):
    if request.method == 'POST':
        form = TransferMoneyForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            accounts = Accounts.objects.all()
            source_account = accounts.get(id=clean_data['source_account'].id)
            target_account = accounts.get(id=clean_data['target_account'].id)
            if source_account.amount >= clean_data['amount'] and not source_account.id == target_account.id:
                source_account.amount -= clean_data['amount']
                target_account.amount += clean_data['amount']
                source_account.save()
                target_account.save()
    return redirect('/zarobki')


@login_required(login_url=login_url)
def credits_view(request):
    credits = Credits.objects.all()
    data = {
        'credits': credits.filter(debt_left__gt=0),
        'new_credit_form': NewCreditForm(),
    }
    return render(request, 'credits.html', data)


@login_required(login_url=login_url)
def add_credit_e(request):
    if request.method == 'POST':
        form = NewCreditForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            print(clean_data['debt_left'])
            credit = Credits()
            credit.name = clean_data['name']
            credit.total_debt = clean_data['total_debt']
            credit.debt_left = clean_data['debt_left']
            credit.repayment = clean_data['repayment']
            credit.number_of_installments = clean_data['number_of_installments']
            credit.installments_payed = clean_data['installments_payed']
            credit.interests = clean_data['installments_payed']
            credit.account = clean_data['account']
            credit.add_credit()
    return redirect('/kredyty')


@login_required(login_url=login_url)
def pay_credit(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            credit_id = int(request.POST['id'])
            credit = Credits.objects.get(id=credit_id)
            account = Accounts.objects.get(id=credit.account.id)

            expense = Expenses()
            expense.name = f'Spłata kredytu: {credit.name}'
            expense.category = 'Inne'
            expense.quantity = 1
            expense.unit_name = 'szt'
            expense.currency = 'zł'
            expense.unit_price = credit.repayment
            expense.total_price = credit.repayment
            expense.charged_account = account
            expense.save()

            account.amount -= credit.repayment
            account.save()
            credit.debt_left -= credit.repayment
            if credit.debt_left <= 0:
                credit.debt_left = 0
            credit.save()

    return redirect('/kredyty')


@login_required(login_url=login_url)
def shopping_list_view(request):
    shopping_list = ShoppingList.objects.all()
    return render(request, 'shopping_list.html', {'shopping_list': shopping_list, 'form': NewShoppingListForm()})


@login_required(login_url=login_url)
def finalize_shopping_list(request):
    print(request.POST)
    for field in enumerate(request.POST):
        if 'bought' in field[1]:
            current_id, _ = field[1].split('_')
            list_element = ShoppingList.objects.get(id=int(current_id))
            current = [x for x in request.POST if current_id in x]
            current_quantityS = request.POST[current[0]].split(',')
            current_costS = request.POST[current[1]].split(',')
            current_quantity = float('.'.join(current_quantityS))
            current_cost = float('.'.join(current_costS))
            expense = Expenses()
            expense.name = list_element.name
            expense.category = list_element.category
            expense.quantity = current_quantity
            expense.unit_price = current_cost
            expense.total_price = current_quantity * current_cost
            expense.currency = 'zł'
            expense.unit_name = list_element.unit_name
            expense.charged_account = list_element.planned_account
            expense.save()
            list_element.delete()
    return redirect('/wydatki')


@login_required(login_url=login_url)
def add_to_shopping_list(request):
    if request.method == 'POST':
        form = NewShoppingListForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            element = ShoppingList()
            element.name = clean_data['name']
            element.quantity = clean_data['quantity']
            element.planned_account = clean_data['planned_account']
            element.category = clean_data['category']
            element.unit_name = clean_data['unit_name']
            element.save()
    return redirect('/lista_zakupow')


@login_required(login_url=login_url)
def delete_shopping_list(request):
    if request.method == 'GET':
        shopping_list = ShoppingList.objects.get(id=request.GET['id'])
        shopping_list.delete()
    return redirect('/lista_zakupow')


@login_required(login_url=login_url)
def planning(request, **kwargs):
    plans = Plan.objects.all().order_by('-date')
    plans_list = []
    for p in plans:
        d = {'plan': p,
            'jedzenie': p.jedzenie/100 * p.predicted_income,
            'chemia': p.chemia/100 * p.predicted_income,
            'kosmetyki': p.kosmetyki/100 * p.predicted_income,
            'dom': p.dom/100 * p.predicted_income,
            'transport': p.transport/100 * p.predicted_income,
            'inne': p.inne/100 * p.predicted_income,
        }
        plans_list.append(d)

    data = {
        'current_year': dt.now().year,
        'current_month': dt.now().month,
        'plans': plans_list
    }

    if 'info' in kwargs:
        data['info'] = kwargs['info']

    return render(request, 'plans.html', data)


@login_required(login_url=login_url)
def add_plan(request):
    months = [None, 'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień',
              'Październik', 'Listopad', 'Grudzień']
    percentesS = request.POST['slider'].split(',')
    percentes = []
    for i in percentesS:
        percentes.append(float(i))

    check_plan = Plan.objects.filter(month=request.POST['month'], year=request.POST['year'])
    print(check_plan)
    if len(check_plan) == 0:
        plan = Plan()
        plan.month = request.POST['month']
        plan.year = request.POST['year']

        plan.date = datetime.date(int(request.POST['year']), int(request.POST['month']), 1)

        plan.jedzenie = percentes[0]
        plan.chemia = percentes[1] - percentes[0]
        plan.kosmetyki = percentes[2] - percentes[1]
        plan.dom = percentes[3] - percentes[2]
        plan.transport = percentes[4] - percentes[3]
        plan.inne = percentes[5] - percentes[4]
        plan.predicted_income = float(request.POST['incomes'])
        plan.add()
        info = f'Dodano plan na {months[plan.date.month]} {plan.date.year}.'
    else:
        info = 'Plan na wybrany miesiąc już istnieje!'
    return planning(request, info=info)


@login_required(login_url=login_url)
def delete_plan(request):
    if request.method == 'POST':
        plan = Plan.objects.get(id=request.POST['id'])
        plan.delete()
    return redirect('/planowanie')

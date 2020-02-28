from django import forms
from .models import Expenses, Incomes, Accounts, Credits, ShoppingList, UnregularPlan


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ('name', 'category', 'quantity', 'currency', 'unit_name', 'unit_price', 'charged_account')
        labels = {
            'name': 'Nazwa produktu',
            'category': 'Kategoria',
            'quantity': 'Ilość',
            'currency': 'Waluta',
            'unit_name': 'Nazwa jednostki',
            'unit_price': 'Cana za jednostkę (zł/j)',
            'charged_account': 'Obciążone konto'
        }

        widgets = {
            'category': forms.Select(
                attrs={'class': 'input-field'},
                choices=[
                    ('Jedzenie', 'Jedzenie'),
                    ('Chemia', 'Chemia'),
                    ('Kosmetyki_Higiena_Leki', 'Kosmetyki, środki higieniczne i lekarstwa'),
                    ('Dom', 'Dom'),
                    ('Transport', 'Transport'),
                    ('Inne', 'Inne')
                ]
            ),
            'unit_name': forms.Select(attrs={'class': 'input-field'}),
        }

class IncomesForm(forms.ModelForm):
    class Meta:
        model = Incomes
        fields = ('name', 'income', 'topped_up_account')

        labels = {
            'name': 'Tytuł wpłaty',
            'income': 'Wartość wpłaty',
            'topped_up_account': 'Zasilone konto'
        }

        widgets = {
            'topped_up_account': forms.Select(attrs={'class': 'input-field'})
        }


class AccountsForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ('accountName', 'accountType', 'amount', 'currency')
        labels = {
            'accountName': 'Nazwa konta',
            'accountType': 'Typ konta',
            'amount': 'Saldo początkowe',
            'currency': 'Waluta'
        }

        widgets = {
            'accountType': forms.Select(attrs={'class': 'input-field'})
        }


class NewCreditForm(forms.ModelForm):
    class Meta:
        model = Credits
        fields = ('name', 'total_debt', 'debt_left', 'repayment', 'number_of_installments', 'installments_payed', 'interests', 'account')
        labels = {
            'name': 'Nazwa kredytu',
            'total_debt': 'Udzielony kredyt (zł)',
            'debt_left': 'Pozostały dług (zł)',
            'repayment': 'Wysokość raty (zł)',
            'number_of_installments': 'Liczba rat',
            'installments_payed': 'Liczba wpłaconych rat',
            'interests': 'Oprocentowanie (%)',
            'account': 'Obciążane konto'
        }


class NewShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ('name', 'quantity', 'planned_account', 'category', 'unit_name')
        labels = {'name': 'Nazwa',
                  'quantity': 'Ilość',
                  'planned_account': 'Konto',
                  'category': 'Kategoria',
                  'unit_name': 'Jednostka'}


class NewUnregularPlan(forms.ModelForm):
    class Meta:
        model = UnregularPlan
        fields = ('name', 'date', 'category', 'value', 'charged_account')
        labels = {'name': 'Nazwa',
                  'date': 'Przewidywana data zakupu',
                  'category': 'Kategoria',
                  'value': 'Przewidywany koszt',
                  'charged_account': 'Konto'}

        widgets = {
            'date': forms.TextInput(attrs={'class': 'datepicker'})
        }


class TransferMoneyForm(forms.Form):
    accounts = Accounts.objects.all()
    source_account = forms.ModelChoiceField(accounts, label='Z konta...', initial=accounts[0])
    target_account = forms.ModelChoiceField(accounts, label='Na konto...', initial=accounts[1])
    amount = forms.FloatField(label='Kwota(zł)')

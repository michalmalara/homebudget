from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete


# Create your models here.

class Accounts(models.Model):
    accountName = models.CharField(max_length=50)
    accountType = models.CharField(max_length=20,
                                   choices=(
                                       ('biezace', 'Rachunek bierzący'),
                                       ('oszczednosciowe', 'Oszczędnościowe'),
                                   ),
                                   default='biezace'
                                   )
    amount = models.FloatField()
    currency = models.CharField(max_length=5, default='zł')

    def add_account(self):
        self.save()

    def __str__(self):
        return f'{self.accountName} ({self.accountType}): {self.amount} {self.currency}'


class Expenses(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(
                                max_length=50,
                                choices=(
                                    ('Jedzenie', 'Jedzenie'),
                                    ('Chemia', 'Chemia'),
                                    ('Kosmetyki_Higiena_Leki', 'Kosmetyki, środki higieniczne i lekarstwa'),
                                    ('Dom', 'Dom'),
                                    ('Transport', 'Transport'),
                                    ('Inne', 'Inne')
                                ),
                                default='Jedzenie'
                            )
    purchase_date = models.DateTimeField(default=timezone.now)
    quantity = models.FloatField()
    unit_name = models.CharField(
                                max_length=5,
                                choices=(
                                    ('szt', 'szt'),
                                    ('kg', 'kg'),
                                    ('l', 'l')
                                ),
                                default='szt'
                            )
    currency = models.CharField(max_length=5, default='zł')
    unit_price = models.FloatField()
    total_price = models.FloatField()
    charged_account = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)


    def add_expense(self):
        self.purchase_date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.name} ({self.category}): {self.total_price} {self.currency}'


class Incomes(models.Model):
    name = models.CharField(max_length=20)
    income = models.FloatField()
    date = models.DateField(default=timezone.now)
    is_cyclic = models.BooleanField()
    topped_up_account = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)

    def add_income(self):
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.date} ({self.name}): {self.income}'


class Credits(models.Model):
    name = models.CharField(max_length=20)
    total_debt = models.FloatField()
    debt_left = models.FloatField()
    repayment = models.FloatField()
    number_of_installments = models.IntegerField()
    installments_payed = models.IntegerField(default=0)
    interests = models.FloatField()
    date = models.DateField(default=timezone.now)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)

    def add_credit(self):
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.name}({self.interests}%): {self.total_debt}'


class ShoppingList(models.Model):
    name = models.CharField(max_length=20)
    planned_account = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)
    quantity = models.FloatField()
    category = models.CharField(
        max_length=50,
        choices=(
            ('Jedzenie', 'Jedzenie'),
            ('Chemia', 'Chemia'),
            ('Kosmetyki_Higiena_Leki', 'Kosmetyki, środki higieniczne i lekarstwa'),
            ('Dom', 'Dom'),
            ('Transport', 'Transport'),
            ('Inne', 'Inne')
        ),
        default='Jedzenie'
    )
    unit_name = models.CharField(
        max_length=5,
        choices=(
            ('szt', 'szt'),
            ('kg', 'kg'),
            ('l', 'l')
        ),
        default='szt'
    )

    def add_list(self):
        self.save()


class Plan(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()

    date = models.DateField()

    jedzenie = models.FloatField()
    chemia = models.FloatField()
    kosmetyki = models.FloatField()
    dom = models.FloatField()
    transport = models.FloatField()
    inne = models.FloatField()

    predicted_income = models.FloatField()

    def add(self):
        self.save()

    def __str__(self):
        return f'Plan: {self.date.month}.{self.date.year}'


class UnregularPlan(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=20)
    value = models.FloatField()
    category = models.CharField(
        max_length=50,
        choices=(
            ('Jedzenie', 'Jedzenie'),
            ('Chemia', 'Chemia'),
            ('Kosmetyki_Higiena_Leki', 'Kosmetyki, środki higieniczne i lekarstwa'),
            ('Dom', 'Dom'),
            ('Transport', 'Transport'),
            ('Inne', 'Inne')
        ),
        default='Inne'
    )
    charged_account = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)
    realized = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.date}): {self.value} zł'

    def add(self):
        self.save()


# Signals handling


def add_expense_handler(sender, **kwargs):
    if kwargs['created']:
        charged_account = kwargs['instance'].charged_account
        account = Accounts.objects.get(accountName=charged_account.accountName)
        account.amount -= kwargs['instance'].total_price
        account.save()


def delete_expense_handler(sender, **kwargs):
    account = kwargs['instance'].charged_account
    account.amount+=kwargs['instance'].total_price
    account.save()


def add_income_handler(sender, **kwargs):
    if kwargs['created']:
        topped_up_account = kwargs['instance'].topped_up_account
        account = Accounts.objects.get(accountName=topped_up_account.accountName)
        account.amount += kwargs['instance'].income
        account.save()


def delete_income_handler(sender, **kwargs):
    account = kwargs['instance'].topped_up_account
    account.amount -= kwargs['instance'].income
    account.save()


post_save.connect(add_expense_handler, sender=Expenses)
post_save.connect(add_income_handler, sender=Incomes)
pre_delete.connect(delete_expense_handler, sender=Expenses)
pre_delete.connect(delete_income_handler, sender=Incomes)

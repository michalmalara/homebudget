from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Expenses)
admin.site.register(models.Incomes)
admin.site.register(models.Accounts)
admin.site.register(models.Credits)
admin.site.register(models.ShoppingList)
admin.site.register(models.Plan)
admin.site.register(models.UnregularPlan)

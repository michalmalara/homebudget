"""budzet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('zaloguj', views.login_view),
    path('do_login', views.do_login),
    path('wyloguj', views.do_logout),
    path('wydatki', views.expenses_view),
    path('dodaj_wydatek', views.add_expense),
    path('add_expense_e', views.do_add_expense),
    path('usun_wydatek', views.delete_expense),
    path('zarobki', views.incomes_view),
    path('add_income_e', views.do_add_income),
    path('usun_wplyw', views.delete_income),
    path('dodaj_konto', views.add_account_e),
    path('przelej_pieniadze', views.transfer_money_e),
    path('kredyty', views.credits_view),
    path('dodaj_kredyt', views.add_credit_e),
    path('splata_raty', views.pay_credit),
    path('usun_kredyt', views.delete_credit),
    path('edytuj_oprocentowanie', views.edit_percentes),
    path('lista_zakupow', views.shopping_list_view),
    path('zrob_zakupy', views.finalize_shopping_list),
    path('dodaj_zakup', views.add_to_shopping_list),
    path('usun_element', views.delete_shopping_list),
    path('planowanie', views.planning, name='planning'),
    path('dodaj_plan', views.add_plan),
    path('usun_plan', views.delete_plan),
    path('dodaj_nieregularny_wydatek', views.add_uplan),
    path('usun_uplan', views.delete_uplan),
    path('zrealizuj_plan', views.realize_plan),
]
urlpatterns += staticfiles_urlpatterns()

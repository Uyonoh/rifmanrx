from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.

def add_credits(request, form) -> None:
    """ Add records for credits """

    credit = Credit(
        item=str(form.instance),
        amount=int(request.POST.get("amount")),
        price=float(request.POST.get("price"))
    )

    credit.save()


def add_debits(request, form) -> None:
    """ Add records for credits """

    debit = Debit(
        item=str(form.instance),
        amount=int(request.POST.get("purchase_amount")),
        price=float(request.POST.get("cost_price"))
    )

    debit.save()

def view_month(request, pk: int=None):
    """ view the current month's records """

    first = tz.datetime(
        year=tz.now().date().year,
        month=tz.now().date().month,
        day=1
    )

    first = first.date() # First day of curent month

    month = BusinessMonth.objects.filter(opening_date__gte=first)

    return render(request, "books/view.html", {"month": month})

def view_sales(request, pk: int):

    month = BusinessMonth.objects.filter(pk=pk)[0]
    sales = month.get_sales()
    print(sales)

    return render(request, "books/sales.html", {"sales": sales})
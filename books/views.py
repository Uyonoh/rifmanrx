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

def first(year: int=tz.now().date().year, month: int=tz.now().date().month) -> tz.datetime:
    """ Returns the first day of a month.
        Defaults to first of current month """
    
    first = tz.datetime(
        year=year,
        month=month,
        day=1
    )

    return first.date()

def view_months(request, pk: int=None):
    """ view the current month's records """

    months = BusinessMonth.objects.all()

    return render(request, "books/view.html", {"months": months})

def view_month(request, pk):
    """ View details for a specific month """

    month = BusinessMonth.objects.filter(pk=pk)

    return render(request, "books/view-month.html", {"month": month})

def view_sales(request, pk: int):

    month = BusinessMonth.objects.filter(pk=pk)[0]
    sales = month.get_sales()

    return render(request, "books/sales.html", {"sales": sales})

def view_purchases(request, pk: int):

    month = BusinessMonth.objects.filter(pk=pk)[0]
    sales = month.get_purchases()

    return render(request, "books/sales.html", {"sales": sales})

def view_credits(request, pk: int):

    month = BusinessMonth.objects.filter(pk=pk)[0]
    sales = month.get_credits()

    return render(request, "books/sales.html", {"sales": sales})

def view_debits(request, pk: int):

    month = BusinessMonth.objects.filter(pk=pk)[0]
    sales = month.get_debits()

    return render(request, "books/sales.html", {"sales": sales})
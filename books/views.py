from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.

def view_months(request):
    return render(request, "books/view.html")

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

    print(debit)
    print(debit.price)
    debit.save()
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

def make_heads(queryset: models.QuerySet) -> list:
    """ Return table headings for a model """

    if queryset.count() < 1:
        return None

    keys = queryset.values()[0].keys()
    keys = list(keys)
    keys.insert(0, "S/N")

    if "drug_id" in keys:
        idx = keys.index("drug_id")
        keys[idx] = "drug"

    return keys

def make_rows(queryset: models.QuerySet) -> dict:

    if queryset.count() < 1:
        return None

    rows = list(queryset.values_list())
    keys = make_heads(queryset)

    for count in range(len(rows)):
        row = list(rows[count])
        row.insert(0, count + 1)
        rows[count] = row

    if "drug" in keys:
        idx = keys.index("drug")

        i = 0
        for count in range(len(rows)):
            row = list(rows[count])
            item = queryset[count]

            row[idx] = item.drug.name
            rows[count] = row

    return rows

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
    total = month.get_sales_price()
    
    heads = make_heads(sales)
    rows = make_rows(sales)

    return render(request, "books/items.html",
                  {"model_query": sales,
                   "title": "Sales",
                   "heads": heads,
                   "rows": rows,
                   "total": total
                   }
                )

def view_purchases(request, pk: int):

    month = BusinessMonth.objects.filter(pk=pk)[0]
    purchases = month.get_purchases()
    total = month.get_purchases_price()

    heads = make_heads(purchases)
    rows = make_rows(purchases)

    return render(request, "books/items.html",
                  {"model_query": purchases,
                   "title": "Purchases",
                   "heads": heads,
                   "rows": rows,
                   "total": total
                   }
                )

def view_credits(request, pk: int):

    month = BusinessMonth.objects.filter(pk=pk)[0]
    credits = month.get_credits()
    total = month.get_credits_price()

    heads = make_heads(credits)
    rows = make_rows(credits)

    return render(request, "books/items.html",
                  {"model_query": credits,
                   "title": "Credits",
                   "heads": heads,
                   "rows": rows,
                   "total": total
                   }
                )

def view_debits(request, pk: int):

    month = BusinessMonth.objects.filter(pk=pk)[0]
    debits = month.get_debits()
    total = month.get_debits_price()

    heads = make_heads(debits)
    rows = make_rows(debits)

    return render(request, "books/items.html",
                  {"model_query": debits,
                   "title": "Debits",
                   "heads": heads,
                   "rows": rows,
                   "total": total
                   }
                )
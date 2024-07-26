from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Drug, Tablet, Suspension, Injectible
from .forms import DrugForm
from books.forms import SaleForm

# Create your views here.

def view_drugs(request):
    drugs = list(Drug.objects.all())
    print(drugs)
    return render(request, "drugs/view-drugs.html", {"drugs": drugs})


# state_dict = {"Tab": "Tablet", "Suspension": "Suspension", "Injectible": "Injectible"}

def view_drug(request, pk):

    drug = Drug.objects.filter(pk=pk).values()[0] # A dict

    return render(request, "drugs/view-drug.html", {"drug": drug})

def add_tab(request, form: DrugForm, update: bool=False) -> None:
    """ Add a tablet drug """

    if not update:
        tab = Tablet(
            drug=form.instance,
            cd_tab=request.POST.get("cd_tab"),
            no_packs=int(request.POST.get("no_packs"))
        )
        tab.save()
    else:
        tab = Tablet(
            drug=form.instance.export(),
            cd_tab=request.POST.get("cd_tab"),
            no_packs=int(request.POST.get("no_packs"))
        )
        
        update_fields = ["purchase_amount", "cost_price"]
        tab.save(
            # drug_update_fields=update_fields,
            price=float(request.POST.get("cost_price")),
            amount=int(request.POST.get("purchase_amount")),
            units=request.POST.get("purchase_units"),
            first_stock=False
            )
        
def add_sus(request, form: DrugForm, update: bool=False) -> None:

    if not update:
        sus = Suspension(
            drug=form.instance,
            no_bottles=int(request.POST.get("no_bottles")),
            # no_packs=request.POST.get("no_packs")
        )
        sus.save()
    else:
        sus = Suspension(
            drug=form.instance.export(),
            no_bottles=int(request.POST.get("no_bottles")),
            # no_packs=request.POST.get("no_packs")
        )
        
        update_fields = ["purchase_amount", "cost_price"]
        sus.save(
            # drug_update_fields=update_fields,
            price=float(request.POST.get("cost_price")),
            amount=int(request.POST.get("purchase_amount")),
            units=request.POST.get("purchase_units"),
            first_stock=False
            )

def add_inj(request, form: DrugForm, update: bool=False) -> None:

    if not update:
        inj = Injectible(
            drug=form.instance,
            no_viles=int(request.POST.get("no_bottles")),
            # no_packs=request.POST.get("no_packs")
        )
        inj.save()
    else:
        inj = Injectible(
            drug=form.instance.export(),
            no_viles=int(request.POST.get("no_bottles")),
            # no_packs=request.POST.get("no_packs")
        )
        
        update_fields = ["purchase_amount", "cost_price"]
        inj.save(
            # drug_update_fields=update_fields,
            price=float(request.POST.get("cost_price")),
            amount=int(request.POST.get("purchase_amount")),
            units=request.POST.get("purchase_units"),
            first_stock=False
            )


def add_drug(request):
    """ Add a drug to the database """

    state_dict = {"Tab": add_tab, "Suspension": add_sus, "Injectable": add_inj}
    print(request)
    if request.method == "POST":
        form = DrugForm(request.POST)

        if form.is_valid():
            print("valid")
            state = form.instance.state
            if not form.instance.exists():
                
                state_dict[state](request, form)
            else:
                state_dict[state](request, form, update=True)
            return HttpResponseRedirect(reverse("drugs:view"))
        print(form.errors)

    else:
        form = DrugForm()
    return render(request, "drugs/add-drug.html", {"form": form})

def restock(request, pk):
    # TODO: Ensure drug attrs cannot be changed in form

    queryset = Drug.objects.filter(pk=pk)
    form = DrugForm()
    form.populate(queryset)

    return render(request, "drugs/add-drug.html", {"form": form})

def sell(request, pk):

    if request.method == "POST":
        form = SaleForm(request.POST)

        if form.is_valid():
            try:
                form.save()
            except ValueError as e:
                form.add_error("amount", e)
                return render(request, "drugs/sell.html", {"form": form})

        # state_dict[state](request, form)

        return HttpResponseRedirect(reverse("drugs:view"))
    
    form = SaleForm()
    drug = Drug.objects.filter(pk=pk)[0]
    form["drug"].initial = drug
    form["price"].initial = drug.price
    form["amount"].initial = 1
    form.set_classes(drug)

    return render(request, "drugs/sell.html", {"form": form})

def edit(request, pk):
    return render(request, "drugs/add.html", {"form": "form"})
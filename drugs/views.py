from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Drug, Tablet
from .forms import DrugForm

# Create your views here.

def view_drugs(request):
    drugs = list(Drug.objects.all())
    print(drugs)
    return render(request, "drugs/view-drugs.html", {"drugs": drugs})


# state_dict = {"Tab": "Tablet", "Suspension": "Suspension", "Injectible": "Injectible"}

def add_tab(request, form: DrugForm, update: bool=False) -> None:
    """ Add a tablet drug """

    if not update:
        tab = Tablet(
            drug=form.instance,
            cd_tab=request.POST.get("cd_tab"),
            no_packs=request.POST.get("no_packs")
        )
        tab.save()
    else:
        tab = Tablet(
            drug=form.instance.export(),
            cd_tab=request.POST.get("cd_tab"),
            no_packs=request.POST.get("no_packs")
        )
        
        update_fields = ["purchase_amount", "cost_price"]
        tab.save(
            # drug_update_fields=update_fields,
            price=int(request.POST.get("cost_price")),
            amount=int(request.POST.get("purchase_amount")),
            units=request.POST.get("purchase_units"),
            first_stock=False
            )


state_dict = {"Tab": add_tab, "Suspension": "Suspension", "Injectible": "Injectible"}

def add_drug(request):
    """ Add a drug to the database """

    if request.method == "POST":
        form = DrugForm(request.POST)

        if form.is_valid():
            state = form.instance.state
            if not form.instance.exists():
                
                state_dict[state](request, form)
            else:
                state_dict[state](request, form, update=True)
            return HttpResponseRedirect(reverse("drugs:view"))

    else:
        form = DrugForm()
    return render(request, "drugs/add-drug.html", {"form": form})
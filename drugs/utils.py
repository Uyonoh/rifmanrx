# Book helpers

import pandas as pd
import os, sys
from .models import Drug, Tablet, Suspension, Injectable
from .forms import DrugForm
from books.views import add_debits, add_purchase


def make_tab(drug, row):
    tab = Tablet(
        drug=drug,
        cd_tab=row.cd_tab,
        no_packs=int(row.no_packs)
    )

    tab.save()

def make_sus(drug, row):
    sus = Suspension(
        drug=drug,
        no_bottles=int(row.no_bottles)
    )

    sus.save()

def make_inj(drug, row):
    inj = Injectable(
        drug=drug,
        no_viles=int(row.no_viles)
    )

    inj.save()

def make_drug(row: pd.Series) -> Drug:

    drug = Drug(
        name=row.name,
        brand_name=row.brand_name,
        mass=int(row.mass),
        state=row.state.capitalize(),
        manufacturer=row.manufacturer,
        exp_date=row.exp_date,
        purchase_amount=int(row.purchase_amount),
        purchase_units=row.purchase_units.capitalize(),
        cost_price=float(row.cost_price),
        category=row.category,
        purpose=row.purpose,
        location=row.location,
    )

    if drug.state == "Tab":
        make_tab(drug, row)
    elif drug.state == "Suspension":
        make_sus(drug, row)
    else:
        make_inj(drug, row)
    
    return drug

class PseudoRequest():
    """ A pseudo html request to deliver pseudo post information """

    def __init__(self, row: pd.Series) -> None:
        self.POST = row.to_dict().copy()

            



def drug_from_csv(path: str) -> None:
    """ Make drug entries from a csv file

    Args:
        path: path to the csv file. """

    # path = "../data/data.csv"
    print("="*28 + " Initializing " + "="*28)

    print("reading file...")
    data = pd.read_csv(path)
    print("done")

    print("="*28 + " Adding drugs " + "="*28)
    for i in range(data.shape[0]):
        row = data.iloc[i]
        row.name = row["name"].upper()
        for field, value in row.items():
            row[field] = str(value).upper()

        print(f"making drug {row.name}...")
        drug = make_drug(row)

        request = PseudoRequest(row)
        form = DrugForm()
        form.instance = drug
        add_purchase(drug, drug.purchase_amount, float(request.POST.get("cost_price")))
        add_debits(request, form)
    print("="*28 + " Finished " + "="*28)
from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import models, Drug, Tablet

class DrugForm(forms.ModelForm):
    """ Drug input form """

    cd_tab = forms.CharField(max_length=30, required=False)
    no_packs = forms.IntegerField(required=False)
    no_bottles = forms.IntegerField(required=False)
    no_viles = forms.IntegerField(required=False)

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs["class"] = "field"

        self.fields["cd_tab"].widget.attrs["class"] += " tab"
        self.fields["no_packs"].widget.attrs["class"] += " tab"
        self.fields["no_bottles"].widget.attrs["class"] += " sus"
        self.fields["no_viles"].widget.attrs["class"] += " inj"

    def populate(self, drug_set: models.QuerySet[Drug]) -> forms.ModelForm:
        drug_dict = drug_set.values()[0]

        for field, value in drug_dict.items():
            if not field in self.Meta.exclude and field != "exp_date":
                self.fields[field].initial = value
        
        state = drug_dict["state"]
        if state == "Tab":
            self.fields["cd_tab"].initial = drug_set[0].get_item_set().cd_tab
            self.fields["no_packs"].initial = drug_set[0].get_item_set().no_packs
        elif state == "Suspension":
            self.fields["no_bottles"].initial = drug_set[0].get_item_set().no_bottles
        else:
            self.fields["no_viles"].initial = drug_set[0].get_item_set().no_viles

    def upper(self) -> None:
        form  = super(DrugForm, self).save(commit=False)

        for field in self.visible_fields():
            try:
                val = getattr(form, field.name)
            except AttributeError:
                continue

            if isinstance(val, str) and field.name != "state":
                setattr(form, field.name, val.upper())
        # form.save()

    # def save(self, commit: bool=False) -> None:
    def save(self, commit: bool = ...) -> Any:
        return super().save(commit)
        
    

    class Meta:
        model = Drug
        # fields = []
        exclude = ["id", "stock_amount", "price", "day_added", "oos"]
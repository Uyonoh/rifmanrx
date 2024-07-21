from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Drug, Tablet

class DrugForm(forms.ModelForm):
    """ Drug input form """

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs["class"] = "field"

        self.fields["cd_tab"].widget.attrs["class"] += " tab"
        self.fields["no_packs"].widget.attrs["class"] += " tab"
        self.fields["no_bottles"].widget.attrs["class"] += " sus"
        self.fields["no_viles"].widget.attrs["class"] += " inj"
        

    # stock_amount = forms.CharField(max_length=30, required=False)
    cd_tab = forms.CharField(max_length=30, required=False)
    no_packs = forms.IntegerField(required=False)
    no_bottles = forms.IntegerField(required=False)
    no_viles = forms.IntegerField(required=False)
    

    class Meta:
        model = Drug
        # fields = []
        exclude = ["id", "stock_amount", "price", "day_added", "oos"]
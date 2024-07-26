from django import forms
from .models import Sale


class SaleForm(forms.ModelForm):
    """ Sale form """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def set_classes(self, drug):
        """ Set form classes """

        self.fields["drug"].widget.attrs["pk"] = f"{drug.pk}"

    

    class Meta:
        model = Sale
        exclude = ["time"]
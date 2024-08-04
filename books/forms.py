from typing import Any
from django import forms
from .models import Sale, Purchase


class SaleForm(forms.ModelForm):
    """ Sale form """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def set_classes(self, drug):
        """ Set form classes """

        self.fields["drug"].widget.attrs["pk"] = f"{drug.pk}"
        self.fields["tab"].widget.attrs["class"] = "check"

    def save(self, commit: bool=True, is_tab: bool=False):
        """
        Save this form's self.instance object if commit=True. Otherwise, add
        a save_m2m() method to the form which can be called after the instance
        is saved manually at a later time. Return the model instance.
        """
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate."
                % (
                    self.instance._meta.object_name,
                    "created" if self.instance._state.adding else "changed",
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            # is_tab = kwargs.get("is_tab")
            self.instance.save(is_tab=is_tab)
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance

    save.alters_data = True

    tab = forms.ChoiceField(choices=(("cd", "Card"), ("tab", "Tab")))


    class Meta:
        model = Sale
        exclude = ["time"]


class PurchaseForm(forms.ModelForm):
    """ Purchase form """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def set_classes(self, drug):
        """ Set form classes """

        self.fields["drug"].widget.attrs["pk"] = f"{drug.pk}"



    class Meta:
        model = Purchase
        exclude = ["time"]
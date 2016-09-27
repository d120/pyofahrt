from django import forms
from .models import Slot

class DuplicateForm(forms.Form):
    slot = forms.ModelChoiceField(queryset=Slot.objects.filter(slottype="workshop"), empty_label=None)

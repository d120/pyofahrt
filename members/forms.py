from django import forms
from django.urls import reverse_lazy
from .models import Member
from ofahrtbase.models import Ofahrt
import datetime

class SignupForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'gender', 'email', 'birth_date', 'food_preference', 'food_handicaps', 'free_text']

    def clean_birth_date(self):
        begin_date = Ofahrt.current().begin_date
        if begin_date.replace(year=begin_date.year - 18) < self.cleaned_data["birth_date"]:
            raise forms.ValidationError("Eine Anmeldung ist nur für Teilnehmer*innen möglich, welche zum Zeitpunkt der Ofahrt volljährig sind.")
        return self.cleaned_data["birth_date"]

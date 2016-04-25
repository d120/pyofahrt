from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(label="Email-Adresse", help_text="Deine Emailadresse brauchen wir, um dir auf deine Anfrage antworten zu können.")
    message = forms.CharField(widget=forms.Textarea, label="Deine Nachricht")

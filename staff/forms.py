from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(label="Email-Adresse", help_text="Deine Emailadresse brauchen wir, um dir auf deine Anfrage antworten zu können.")
    message = forms.CharField(widget=forms.Textarea, label="Deine Nachricht")



class PasswordForm(forms.Form):
    oldpassword = forms.CharField(label="Altes Passwort", widget=forms.PasswordInput)
    newpassworda = forms.CharField(label="Neues Passwort", widget=forms.PasswordInput)
    newpasswordb = forms.CharField(label="Neues Passwort wiederholen", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        data = self.cleaned_data['oldpassword']
        correct = self.user.check_password(data)
        if not correct:
            raise forms.ValidationError("Dein altes Passwort ist nicht korrekt.", code="oldpwwrong")

    def clean_newpasswordb(self):
        dataa = self.cleaned_data['newpassworda']
        datab = self.cleaned_data['newpasswordb']
        if not dataa == datab:
            raise forms.ValidationError("Die beiden Passwörter stimmen nicht miteinander überein.", code="differentnewpasswords")

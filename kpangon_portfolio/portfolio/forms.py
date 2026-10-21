from django import forms

from .models import ContactMessage

_BASE = (
    "w-full rounded-lg border border-slate-300 bg-white px-4 py-3 text-slate-800 "
    "placeholder-slate-400 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/30 focus:outline-none"
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["nom", "email", "sujet", "message"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": _BASE, "placeholder": "Votre nom complet"}),
            "email": forms.EmailInput(attrs={"class": _BASE, "placeholder": "vous@exemple.com"}),
            "sujet": forms.TextInput(attrs={"class": _BASE, "placeholder": "Objet de votre message"}),
            "message": forms.Textarea(attrs={"class": _BASE, "rows": 5, "placeholder": "Votre message…"}),
        }

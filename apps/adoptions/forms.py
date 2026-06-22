from django import forms

from .models import AdoptionApplication


class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ("motivation", "housing", "experience", "contact")
        widgets = {
            "motivation": forms.Textarea(attrs={"rows": 4}),
            "experience": forms.Textarea(attrs={"rows": 4}),
        }

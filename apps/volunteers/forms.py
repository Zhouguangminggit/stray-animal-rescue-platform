from pathlib import Path

from django import forms

from .models import CommunityPost, CommunityReport, VolunteerApplication


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ("intention", "skills", "availability", "experience", "material")
        widgets = {
            "intention": forms.Textarea(attrs={"rows": 4}),
            "experience": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_material(self):
        material = self.cleaned_data.get("material")
        if not material:
            return material
        if material.size > 10 * 1024 * 1024:
            raise forms.ValidationError("材料不能超过 10MB。")
        if Path(material.name).suffix.lower() not in {
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }:
            raise forms.ValidationError("仅支持 PDF、JPG、PNG 或 WebP 材料。")
        return material


class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ("title", "content")
        widgets = {"content": forms.Textarea(attrs={"rows": 8})}


class CommunityReportForm(forms.ModelForm):
    class Meta:
        model = CommunityReport
        fields = ("reason",)
        widgets = {"reason": forms.Textarea(attrs={"rows": 4})}

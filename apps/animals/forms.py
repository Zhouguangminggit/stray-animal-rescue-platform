from typing import cast

from django import forms

from apps.campuses.models import Campus

from .models import AnimalCategory, RescueRequest


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        files = data if isinstance(data, (list, tuple)) else [data] if data else []
        if len(files) > 6:
            raise forms.ValidationError("最多上传 6 张图片。")
        parent_clean = super().clean
        cleaned = [parent_clean(item, initial) for item in files]
        for image in cleaned:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("单张图片不能超过 5MB。")
            if getattr(image, "content_type", "") not in {
                "image/jpeg",
                "image/png",
                "image/webp",
            }:
                raise forms.ValidationError("仅支持 JPG、PNG 或 WebP 图片。")
        return cleaned


class RescueRequestForm(forms.ModelForm):
    images = MultipleImageField(
        label="动物图片", required=False, help_text="最多 6 张，单张不超过 5MB。"
    )

    class Meta:
        model = RescueRequest
        fields = (
            "category",
            "animal_name",
            "gender",
            "health_status",
            "campus",
            "found_location",
            "description",
            "contact",
        )
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_field = cast(forms.ModelChoiceField, self.fields["category"])
        campus_field = cast(forms.ModelChoiceField, self.fields["campus"])
        category_field.queryset = AnimalCategory.objects.filter(is_active=True)
        campus_field.queryset = Campus.objects.filter(
            is_active=True, school__is_active=True
        )

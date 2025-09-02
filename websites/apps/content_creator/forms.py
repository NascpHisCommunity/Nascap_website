from django import forms
from .models import Content, Category

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = "__all__"
        widgets = {
            # CKEditor widget is auto-applied by the model field; we only style other fields here
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Optional category description"}),
        }

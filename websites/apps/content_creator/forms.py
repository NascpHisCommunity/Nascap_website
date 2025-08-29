from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Content, Category

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = "__all__"
        widgets = {
            "body": SummernoteWidget(),                      # ← swapped editor
            "published_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }

class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating content categories.
    """
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional category description'}),
        }

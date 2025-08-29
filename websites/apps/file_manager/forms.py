from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import File

class FileUploadForm(forms.ModelForm):
    """
    A ModelForm for uploading files with metadata. It uses crispy_forms
    to provide a cleaner layout and better form rendering.
    """
    class Meta:
        model = File
        fields = ['title', 'description', 'file', 'category', 'file_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter a description of the file'}),
        }
        labels = {
            'title': 'File Title',
            'description': 'Description',
            'file': 'Select File',
            'category': 'Category',
            'file_type': 'File Type',
        }

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Field('file'),
            Field('category'),
            Field('file_type'),
            Submit('submit', 'Upload File', css_class='btn btn-primary')
        )

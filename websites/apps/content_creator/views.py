from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Content, Category
from .forms import ContentForm, CategoryForm

# Content Views
class ContentListView(ListView):
    model = Content
    template_name = 'content_creator/content_list.html'
    context_object_name = 'contents'
    paginate_by = 10

class ContentDetailView(DetailView):
    model = Content
    template_name = 'content_creator/content_detail.html'
    context_object_name = 'content'

class ContentCreateView(CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'content_creator/content_form.html'
    success_url = reverse_lazy('content_creator:content_list')

class ContentUpdateView(UpdateView):
    model = Content
    form_class = ContentForm
    template_name = 'content_creator/content_form.html'
    success_url = reverse_lazy('content_creator:content_list')

class ContentDeleteView(DeleteView):
    model = Content
    template_name = 'content_creator/content_confirm_delete.html'
    success_url = reverse_lazy('content_creator:content_list')


# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'content_creator/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'content_creator/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'content_creator/category_form.html'
    success_url = reverse_lazy('content_creator:category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'content_creator/category_form.html'
    success_url = reverse_lazy('content_creator:category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'content_creator/category_confirm_delete.html'
    success_url = reverse_lazy('content_creator:category_list')

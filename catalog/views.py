from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView
from catalog.models import Product, Category, Version
from catalog.forms import ProductForm, CategoryForm, VersionForm
from django.urls import reverse_lazy
from config.utils import ValidMixin, VersionViewMixin


class IndexTemplateView(VersionViewMixin, TemplateView):
    model = Product
    success_url = reverse_lazy('catalog:index')


def contacts(request):
    return render(request, 'catalog/contacts.html')


class ProductCreateView(ValidMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:category_list')


class ProductListView(VersionViewMixin, ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Product.objects.filter(category_id=category_id)


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_version: Version = Version.objects.filter(product=self.object, is_active=True).last()
        if active_version:
            context['is_active'] = active_version.is_active
            context['version'] = active_version.version
            context['name_version'] = active_version.name_version
        else:
            context['version'] = None
            context['name_version'] = None

        return context


class ProductUpdateView(ValidMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:category_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:category_list')


class CategoryCreateView(ValidMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Обработка описания категорий
        for category in context['categories']:
            if len(category.description) > 100:
                category.description = category.description[:100] + '...'  # Ограничение до 100 символов

        return context


class CategoryDetailView(DetailView):
    model = Product
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CategoryUpdateView(ValidMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('catalog:category_list')


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:category_list')

from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from catalog.models import Product, Category, Version
from catalog.forms import ProductForm, CategoryForm
from django.urls import reverse_lazy


def index(request):
    context = {
        'object_list': Product.objects.all()[:3],
        'title': 'Топ товаров'
    }

    return render(request, 'catalog/product_list.html', context)


def contacts(request):
    return render(request, 'catalog/contacts.html')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        if image:
            new_product = form.save(commit=False)
            new_product.image = image
            new_product.save()
        else:
            form.save()

        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for product in context['object_list']:
            active_version: Version = Version.objects.filter(product=product, is_active=True).last()
            if active_version:
                product.is_active = active_version.is_active
                product.version = active_version.version
                product.name_version = active_version.name_version
            else:
                product.version = None
                product.name_version = None

        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_version: Version = Version.objects.filter(product=self.object, is_active=True).last()
        if active_version:
            context['number'] = active_version.version
            context['name_version'] = active_version.name
        else:
            context['number'] = None
            context['name_version'] = None

        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        if image:
            new_product = form.save(commit=False)
            new_product.image = image
            new_product.save()
        else:
            form.save()

        return super().form_valid(form)


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


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('catalog:category_list')

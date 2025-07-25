from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .forms import ProductForm
from .models import Product
from .models import Order
from .forms import GroupForm

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            'products': products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)
    
class GroupsListViev(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)
    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)
    
# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             'product': product,
#         }
#         return render(request, 'shopapp/products-details.html', context=context)

class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    # queryset = Product.objects.prefetch_related('orders')
    context_object_name = 'product'

# class ProductListView(TemplateView):
#     template_name = 'shopapp/products-list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         return context

class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)

# def products_list(request):
#     context = {
#         'products': Product.objects.all(),
#     }
#     return render(request, 'shopapp/products-list.html', context=context)


# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             #name = form.cleaned_data['name']
#             #price = form.cleaned_data['price']
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse('shopapp:products_list')
#             return redirect(url)
#     else:
#         form = ProductForm(request.POST)
#     context = {
#         'form': form,
#     }
#     return render(request, 'shopapp/create-product.html', context=context)

class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

# def orders_list(request):
#     context = {
#         'orders': Order.objects.select_related('user').prefetch_related("products").all(),

#     }
#     return render(request, 'shopapp/orders-list.html', context=context)

# class OrdersListView(LoginRequiredMixin, ListView):
#     queryset = (
#         Order.objects
#         .select_related('user')
#         .prefetch_related("products")
#     )

class OrdersListView(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('orders.view_order'):
            return Order.objects.select_related('user').prefetch_related("products")
        return Order.objects.filter(user=user).select_related('user').prefetch_related("products")

# class OrderDetailView(PermissionRequiredMixin, DetailView): # PermissionRequiredMixin не работает
#     permission_required = 'shopapp.view_order'
#     queryset = (
#         Order.objects
#         .select_related('user')
#         .prefetch_related("products")
#     )

class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    queryset = Order.objects.select_related('user').prefetch_related('products')

    def test_func(self):
        order = self.get_object()
        user = self.request.user
        return user == order.user or user.has_perm('shopapp.view_order')  

class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)
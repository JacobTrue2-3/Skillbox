from django.urls import path

from .views import ( 
    ShopIndexView, 
    GroupsListViev,
    ProductDetailsView,
    ProductListView,
    OrdersListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView)


app_name = 'shopapp'

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('groups/', GroupsListViev.as_view(), name='groups'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('orders/', OrdersListView.as_view(), name='order_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archived/', ProductDeleteView.as_view(), name='product_delete'), 
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
]
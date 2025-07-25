from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest


from .models import Product, Order
from .admin_mixins import ExportAsCSCMixin

# admin.site.register(Product, ProductAdmin) Альтернатива регистрации без "@admin.register"
# admin.site.register(Order)

class OrderInline(admin.TabularInline):
    model = Product.orders.through

@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSCMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        ExportAsCSCMixin.export_csv,
    ]

    inlines = [
        OrderInline,
    ]
    list_display = 'pk', 'name', 'price', 'description_short', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = '-name', 'pk'
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse'),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is for soft delete',
        })
    ]

    def  description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '  ...'
    
#class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'
    list_display_links = 'delivery_address',
    ordering = '-created_at',
    search_fields = 'promocode',

    inlines = [
        ProductInline,
    ]

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')
    
    
    # def user_verbose(self, obj: Order) -> str: альтернатива функции ниже
    #     return obj.user.first_name or obj.user.username

    def user_verbose(self, obj: Order) -> str:
        user = obj.user
        if not user:
            return "—"
        
        # Собираем части имени
        name_parts = []
        if user.first_name:
            name_parts.append(user.first_name)
        if user.last_name:
            name_parts.append(user.last_name)
        
        # Если есть хотя бы first_name или last_name - объединяем их
        if name_parts:
            return " ".join(name_parts)
        
        # Если нет ни first_name ни last_name - возвращаем username
        return user.username

    user_verbose.short_description = "User"  # Заголовок для колонки в админке



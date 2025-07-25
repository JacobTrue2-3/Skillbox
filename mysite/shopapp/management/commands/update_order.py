from django.core.management.base import BaseCommand

from shopapp.models import Order, Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('No orders')
            return
        products = Product.objects.all()

        for product in products:
            order.products.add(product)

        order.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added products to order {order.products.all()} to order {order}'
                )
        )
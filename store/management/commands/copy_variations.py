from django.core.management.base import BaseCommand
from store.models import Product, Variation


class Command(BaseCommand):
    help = 'Copy price variations from "bong-ro-chuyen-nghiep" product to all other products'

    def handle(self, *args, **options):
        # Find the source product (bóng rổ chuyên nghiệp vba)
        source = Product.objects.filter(slug__icontains='bong-ro-chuyen-nghiep').first()
        if not source:
            self.stdout.write(self.style.ERROR(
                'Source product not found. Make sure a product with "bong-ro-chuyen-nghiep" in its slug exists.'
            ))
            return

        source_variations = Variation.objects.filter(product=source, variation_category='price', is_active=True)
        values = list(source_variations.values_list('variation_value', flat=True))

        if not values:
            self.stdout.write(self.style.ERROR(f'No price variations found for "{source.product_name}".'))
            return

        self.stdout.write(f'Source: {source.product_name}')
        self.stdout.write(f'Price options: {values}')

        other_products = Product.objects.exclude(id=source.id)
        created_count = 0

        for product in other_products:
            for value in values:
                _, created = Variation.objects.get_or_create(
                    product=product,
                    variation_category='price',
                    variation_value=value,
                    defaults={'is_active': True},
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created {created_count} new variation(s) across {other_products.count()} product(s).'
        ))

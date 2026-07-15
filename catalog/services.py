from django.core.cache import cache

from catalog.models import Category, Product


CATEGORY_CACHE_TTL = 60 * 15


def get_products_by_category(category_id):
    cache_key = f"category_{category_id}"

    products = cache.get(cache_key)

    if products is None:
        category = Category.objects.get(pk=category_id)

        products = list(
            Product.objects.filter(
                category=category
            ).select_related(
                "category",
                "owner",
            )
        )

        cache.set(
            cache_key,
            products,
            CATEGORY_CACHE_TTL,
        )

    return products

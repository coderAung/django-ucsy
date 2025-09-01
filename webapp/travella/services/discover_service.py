from travella.models import Category, Package, Review

def get_discover_data():
    categories_count = Category.objects.count()
    packages_count = Package.objects.count()
    reviews_count = Review.objects.count()

    return {
        'categories_count': categories_count,
        'packages_count': packages_count,
        'reviews_count': reviews_count,
    }

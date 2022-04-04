from store.models import ProductModel, ReviewRatingModel
from django.db.models import Avg


def populer_products_list(request):
    populer_products = ProductModel.objects.filter(reviews__rating__isnull=False).\
        annotate(Avg("reviews__rating")).order_by("-reviews__rating")[:8]

    return {"populer_products":populer_products}

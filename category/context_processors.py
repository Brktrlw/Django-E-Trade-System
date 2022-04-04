from .models import CategoryModel

def menu_links(request):
    categories = CategoryModel.objects.all()
    return dict(categories=categories)
from django.shortcuts import render
from katalog.models import CatalogItem


# Create your views here.
def show_katalog(request):
    data_katalog_item = CatalogItem.objects.all()
    context = {
        'list_item': data_katalog_item,
        'name': 'Jovian',
        'student_id': '2106720891'
    }

    return render(request, "katalog.html", context)


# TODO: Create your views here.

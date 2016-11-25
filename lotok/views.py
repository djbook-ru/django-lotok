
from django.shortcuts import render, get_object_or_404

from lotok.models import Category, Product


def index(request):
    return render(request, 'tstapp/index.html', {
        'categories': Category.objects.all()
    })


def category(request, name):
    return render(request, 'tstapp/category.html', {
        'category': get_object_or_404(Category, name=name)
    })


def product(request, name):
    return render(request, 'tstapp/product.html', {
        'product': get_object_or_404(Product, name=name)
    })
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

def home_page(request):
    return render(request, "home.html")

def new_list(request):
    Item.objects.create(
        text = request.POST['item_text'],
        list = List.objects.create()
    )

    return redirect('/lists/the-only-list-in-the-world/')

def view_list(request):
    view_list_template = "list.html"
    return render(
        request,
        view_list_template,
        { 
            'items': Item.objects.all()
        }
    )
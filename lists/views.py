from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

def home_page(request):
    return render(request, "home.html")

def new_list(request):
    created_list = List.objects.create()

    Item.objects.create(
        text = request.POST['item_text'],
        list = created_list
    )

    return redirect(f'/lists/{created_list.id}/')

def add_item(request, list_id):
    recovered_list = List.objects.get(id = list_id)

    Item.objects.create(
        text = request.POST['item_text'],
        list = recovered_list
    )

    return redirect(f'/lists/{recovered_list.id}/')

def view_list(request, list_id):
    recovered_list = List.objects.get(id = list_id)

    return render(
        request,
        "list.html",
        { 
            'list': recovered_list
        }
    )
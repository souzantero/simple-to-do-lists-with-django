from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List

def home_page(request):
    return render(request, "home.html")

def new_list(request):
    created_list = List.objects.create()
    item = Item(
        text = request.POST['item_text'],
        list = created_list
    )

    try:
        item.full_clean()
        item.save()
    except ValidationError:
        created_list.delete()
        
        error = "You can't have an empty list item"
        return render(request, 'home.html', {
            'error': error
        })

    return redirect(f'/lists/{created_list.id}/') 

def view_list(request, list_id):
    recovered_list = List.objects.get(id = list_id)

    if request.method == 'POST':
        Item.objects.create(
            text = request.POST['item_text'],
            list = recovered_list
        )
        
        return redirect(f'/lists/{recovered_list.id}/')

    return render(
        request,
        "list.html",
        { 
            'list': recovered_list
        }
    )
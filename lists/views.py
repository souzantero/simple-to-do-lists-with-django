from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
from lists.models import Item, List

def home_page(request):
    return render(request, "home.html", { 'form': ItemForm() })

def new_list(request):
    form = ItemForm(data = request.POST)
    
    if form.is_valid():
        created_list = List.objects.create()
        Item.objects.create(
            text = request.POST['text'],
            list = created_list
        )

        return redirect(created_list)
    else:
        return render(request, 'home.html', { 'form': form })

def view_list(request, list_id):
    recovered_list = List.objects.get(id = list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data = request.POST)
        if form.is_valid():
            Item.objects.create(text = request.POST['text'], list = recovered_list)
            return redirect(recovered_list)
    
    return render(request, 'list.html', {
        'list': recovered_list,
        'form': form
    })
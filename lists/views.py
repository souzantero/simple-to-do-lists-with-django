from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

def home_page(request):
    home_page_template = "home.html"

    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')

    return render(
        request, 
        home_page_template
    )

def view_list(request):
    view_list_template = "list.html"
    return render(
        request,
        view_list_template,
        { 
            'items': Item.objects.all()
        }
    )
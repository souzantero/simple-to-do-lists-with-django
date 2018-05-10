from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

def home_page(request):
    home_page_name = "home.html"

    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('/')

    return render(
        request, 
        home_page_name,
        {
            'items': Item.objects.all()
        }
    )
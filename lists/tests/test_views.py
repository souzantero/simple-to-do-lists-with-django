from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
    def test_use_home_template(self):
        self.assertTemplateUsed(
            self.client.get('/'),
            'home.html'
        )

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        new_list = List.objects.create()
        response = self.client.get(f'/lists/{new_list.id}/')

        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()

        Item.objects.create(text = 'itemey 1', list = correct_list)
        Item.objects.create(text = 'itemey 2', list = correct_list)

        another_list = List.objects.create()

        Item.objects.create(text = 'Another list item 1', list = another_list)
        Item.objects.create(text = 'Another list item 2', list = another_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'Another list item 1')
        self.assertNotContains(response, 'Another list item 2')

    def test_passes_correct_list_to_template(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(
            Item.objects.first().text,
            'A new list item'
        )

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={ 'item_text': 'A new list item' })
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data = { 'item_text': 'A new item for an existing list' }
        )

        self.assertEqual(Item.objects.count(), 1)
        
        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        another_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data = { 'item_text': 'A new item for an existing list' }
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
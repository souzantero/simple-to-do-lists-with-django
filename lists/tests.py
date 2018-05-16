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
    def test_displays_all_items(self):
        new_list = List.objects.create()

        Item.objects.create(text = 'itemey 1', list = new_list)
        Item.objects.create(text = 'itemey 2', list = new_list)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(
            Item.objects.first().text,
            'A new list item'
        )

    def test_redirect_after_POST(self):
        self.assertRedirects(
            self.client.post(
                '/lists/new', 
                data={
                    'item_text': 'A new list item'
                }),
            '/lists/the-only-list-in-the-world/')

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        new_list = List()
        new_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = new_list
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = new_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, new_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, new_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, new_list)

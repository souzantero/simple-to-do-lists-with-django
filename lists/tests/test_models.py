from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        new_list = List.objects.create()
        item = Item()
        item.list = new_list
        item.save()
        
        self.assertIn(item, new_list.item_set.all())

    def test_cannot_save_empty_list_items(self):
        new_list = List.objects.create()
        item = Item(list = new_list, text = '')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        new_list = List.objects.create()
        Item.objects.create(list = new_list, text = 'bla')

        with self.assertRaises(ValidationError):
            item = Item(list = new_list, text = 'bla')
            item.full_clean()

    def test_can_save_same_item_to_differents_lists(self):
        first_list = List.objects.create()
        second_list = List.objects.create()

        Item.objects.create(list = first_list, text = 'bla')

        item = Item(list = second_list, text = 'bla')
        item.full_clean() # NÃO deve gerar erro

    def test_list_ordering(self):
        new_list = List.objects.create()
        first_item = Item.objects.create(list = new_list, text = 'i1')
        second_item = Item.objects.create(list = new_list, text = 'item 2')
        third_item = Item.objects.create(list = new_list, text = '3')

        self.assertEqual(
            list(Item.objects.all()),
            [first_item, second_item, third_item]
        )
    
    def test_string_representation(self):
        item = Item(text = 'some text')
        self.assertEqual(str(item), 'some text')

class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        new_list = List.objects.create()
        self.assertEqual(new_list.get_absolute_url(), f'/lists/{new_list.id}/')

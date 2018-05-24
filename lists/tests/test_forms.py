from django.test import TestCase
from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)

class ItemFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data = { 'text': '' })
        
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_save_handles_saving_to_a_list(self):
        created_list = List.objects.create()
        form = ItemForm(data = { 'text': 'do me' })
        new_item = form.save(for_list = created_list)

        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, created_list)

class ExistingListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        new_list = List.objects.create()
        form = ExistingListItemForm(for_list = new_list)
        
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        new_list = List.objects.create()
        form = ExistingListItemForm(for_list = new_list, data = { 'text': '' })
        
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_validation_for_duplicate_items(self):
        created_list = List.objects.create()
        Item.objects.create(list = created_list, text = 'no twins!')
        form = ExistingListItemForm(for_list = created_list, data = { 'text': 'no twins!' })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
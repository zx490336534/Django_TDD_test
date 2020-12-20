# 运行单元测试:python manage.py test lists
from django.test import TestCase
from lists.models import Item


class SmokeTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': "一项新事项"})
        self.assertEqual(Item.objects.count(), 1)
        print(Item.objects.all())
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "一项新事项")
        self.assertIn("一项新事项", response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):
    def test_saveing_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '第一条待办事项'
        first_item.save()

        second_item = Item()
        second_item.text = '第二条待办事项'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '第一条待办事项')
        self.assertEqual(second_saved_item.text, '第二条待办事项')


class HomePageTest(TestCase):
    def test_only_saves_items_when_necessart(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': '一个新待办事项'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '一个新待办事项')

    def test_refirects_after_POST(self):
        response = self.client.post('/', data={'item_text': '一个新待办事项1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    
class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

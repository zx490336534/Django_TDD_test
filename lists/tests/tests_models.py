# 运行单元测试:python manage.py test lists
from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelsTest(TestCase):
    def test_saveing_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = '第一条待办事项'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = '第二条待办事项'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '第一条待办事项')
        self.assertEqual(second_saved_item.text, '第二条待办事项')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.list, list_)

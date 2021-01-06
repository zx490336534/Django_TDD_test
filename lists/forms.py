# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 下午10:01
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : forms.py
from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "你不能创建一个空待办事项"


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': "请输入待办事项",
                    'class': 'form-control input-lg'
                }
            )
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

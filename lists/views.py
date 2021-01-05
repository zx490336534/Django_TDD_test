from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.html import escape

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = '你不能创建一个空待办事项'
    return render(request, 'list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        # escape 防止出现转义问题
        error = escape('你不能创建一个空待办事项')
        return render(request, 'home.html', {"error": error})
    return redirect(list_)  # 等价于 return redirect('view_list', list_.id)

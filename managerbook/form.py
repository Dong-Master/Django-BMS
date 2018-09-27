#coding:utf-8
#@mail:879995812@qq.com

from django import forms
from django.forms import widgets
from .models import TypeBook, Publisher, Author
# 定义组件和样式
#用来渲染前台的html页面的css样式
# id是一定要给的,后面的ajax是需要用到id的
class BookForm(forms.Form):
    """
        图书添加表单
    """
    name = forms.CharField(
        max_length=32,
        min_length=2,
        widget=widgets.TextInput(
            attrs={"op": '冬梅', "class": 'form-control', "id": 'bookname', "placeholder": "书名"}
        )
    )
    publish_year = forms.DateField(
        widget=widgets.DateInput(
            attrs={"placeholder": "出版日期: 2017-1-1", "class": "form-control", "id": "publish_year"}
        )
    )

    price = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "价格", "class": 'form-control', "id": "price"}
        )
    )

    stocks = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "库存", "class": 'form-control', "id": "stocks"}
        )
    )

    author = forms.MultipleChoiceField(
        choices=Author.objects.all().values_list('id', 'name'),
        widget=widgets.SelectMultiple(
            # attrs={"class": "demo-cs-multiselect","id":"author"}
            attrs={"id": "demo-cs-multiselect"}
        )
    )

    status = forms.ChoiceField(
        choices=[(1, "出版"), (0, '未出版')],
        widget=widgets.Select(
            attrs={"class": "magic-select", "type": "select", "id": 'status', }
        )

    )

    type = forms.ChoiceField(
        choices=TypeBook.objects.all().values_list('id', 'type_book'),
        widget=widgets.Select(
            attrs={"class": "selectpicker", "data-live-search": "true", "data-width": "100%", "id": "type", }
        )
    )

    publisher = forms.ChoiceField(
        choices=Publisher.objects.all().values_list('id', 'name'),
        widget=widgets.Select(
            attrs={"class": "selectpicker", "data-live-search": "true", "data-width": "100%", "id": "publisher", }
        )
    )

    # ==============================================
    # choices的固定格式,quaryset集合,[(id,"变量"),(id,"变量")]   可选择的部分

class DetailsForm(forms.Form):        #用来完善图书详情
    """
       图书详情表单
    """
    chapter = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "章节", "class": "form-control", 'id': 'chapter', }
        )
    )

    pages = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "页数", "class": "form-control", 'id': 'pages', }
        )
    )

    words = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={"placeholder": "字数", "class": "form-control", 'id': 'words', }
        )
    )

    contentinfo = forms.CharField(
        widget=widgets.Textarea(
            attrs={"rows": 8, "class": 'form-control', "id": "demo-textarea-input-1", 'placeholder': '内容简介'}
        )
    )

    catalog = forms.CharField(
        widget=widgets.Textarea(
            attrs={"rows": 8, "class": 'form-control', "id": "demo-textarea-input-2", 'placeholder': '目录'}
        )
    )

    logo = forms.ImageField(
        required=False,
        widget=widgets.FileInput(
            attrs={"id": "logo_file", "class": 'fileinput-new btn btn-primary btn-file'}
        )
    )
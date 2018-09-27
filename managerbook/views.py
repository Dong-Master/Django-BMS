from django.shortcuts import render
from django.views.generic import ListView, View
from managerbook.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from managerbook.form import *
from django.http import JsonResponse
from PIL import Image
from django.forms import model_to_dict


# Create your views here.
#
class Addbook(ListView):
    template_name = 'add_book.html'
    model = Book
    context_object_name = 'book_obj'

    def get_queryset(self):

        queryset = super(Addbook, self).get_queryset().order_by('id')
        page = self.request.GET.get('page', 1)
        p = Paginator(queryset, 10)
        people = p.page(page)

        return people

    def get_context_data(self, **kwargs):

        book_form = BookForm()
        details_form = DetailsForm()
        context = super(Addbook, self).get_context_data()

        context['book_form'] = book_form
        context['details_form'] = details_form

        return context

    def post(self, request):

        ret = {"status": "", "data": ""}
        # print(request.POST)
        # print(self.request.POST)
        book_form = BookForm(request.POST)

        if book_form.is_valid():
            book_data = book_form.cleaned_data
            book = Book()
            book.name = book_data['name']
            book.publish_year = book_data['publish_year']
            book.price = book_data['price']
            book.stocks = book_data['stocks']
            book.status = book_data['status']
            book.type_id = book_data['type']  # 拿到的是id，所以用id存储，不用对象存储
            book.publisher_id = book_data['publisher']
            # book.author = book_data['author']
            book.save()
            book.author.add(*book_data['author'])  # *代表存列表格式
            ret['status'] = "success"
            ret['data'] = "书籍添加成功"
        else:
            # print(book_form.errors)
            """
            {
                'status':"",
                'data':"{"price":"必须要填写的字段"},"                
            }
            """
            ret['data'] = book_form.errors
        return JsonResponse(ret)


class index(ListView):  # 默认的get方法

    template_name = 'book.html'  # 在哪个模板展示
    model = Book  # 展示的是哪一张表
    context_object_name = 'book_obj'

    # print(Book)
    def get_queryset(self):
        # ================================================
        # super调用父类的
        queryset = super(index, self).get_queryset().order_by("id")
        # UnorderedObjectListWarning: Pagination may yield inconsistent results with a
        # 出现的错误，在后面加上order_by("id")或者其他的排序就可以了

        # print(self.request.GET)
        # print(queryset)
        # queryset = Book.object.all()
        # queryset就是等同于Book所有的值
        # ================================================
        page = self.request.GET.get('page', 1)
        # 第一个参数 数据[] list
        # 第二个参数 一页展示多少条

        self.is_type = self.request.GET.get('type', '')  # 前面是传递过来的name，后面是默认值
        self.is_status = self.request.GET.get('status', '')
        self.search = self.request.GET.get('search', '')  # 而字符串则不必要担心

        # Q多种条件查询 and == ,或者|
        # or == |

        if self.is_type and self.is_status:  # 这两个字段传递的是整型数据，如果默认为空会出错
            queryset = self.model.objects.filter(  # self.model == Book 上面声明过
                (Q(name__icontains=self.search) | Q(author__name__icontains=self.search))
                & Q(type=self.is_type) & Q(status=self.is_status)
            ).distinct()
        elif self.is_type:
            queryset = self.model.objects.filter(
                (Q(name__icontains=self.search) | Q(author__name__icontains=self.search))
                & Q(type=self.is_type)
            ).distinct()
        elif self.is_status:
            queryset = self.model.objects.filter(
                (Q(name__icontains=self.search) | Q(author__name__icontains=self.search))
                & Q(status=self.is_status)
            ).distinct()
        elif self.search and (self.is_type == '' and self.is_status == ''):
            queryset = self.model.objects.filter(
                (Q(name__icontains=self.search) | Q(author__name__icontains=self.search))
            ).distinct()

        p = Paginator(queryset, 10)
        people = p.page(page)

        return people

    def get_context_data(self, **kwargs):
        # ================================================
        type_all = TypeBook.objects.all()  # 读取TypeBook表的内容
        # print(type_all)
        # 在上下文信息中，将获取到的类型加入字典，前端可以调用。
        context = super(index, self).get_context_data(**kwargs)
        context['type_all'] = type_all
        try:  # 通过异常处理忽略错误
            context['is_type'] = int(self.is_type)
        except:
            context['is_type'] = ''

        try:
            context['is_status'] = int(self.is_status)
        except:
            pass

        context['search'] = self.search
        # print(context)

        return context


class Create_Details(View):
    """
    完善书籍详情页功能
    """

    def post(self, request):

        ret = {'status': '', 'data': ''}
        details_form = DetailsForm(request.POST, request.FILES)  # 设计文件、图片的提交，增加一个FILES
        # print(details_form)
        if details_form.is_valid():
            # print(details_form.errors)
            details_data = details_form.cleaned_data
            details = Details()
            details.chapter = details_data['chapter']
            details.contentinfo = details_data['contentinfo']
            details.catalog = details_data['catalog']
            details.words = details_data['words']
            details.pages = details_data['pages']

            try:
                # 保存图片或者文件到本地
                logo = details_data['logo']
                location = 'media/images/logos/' + \
                           str(details_data['words']) + str(details_data['pages']) + '_' + str(logo.name)
                img = Image.open(logo)
                img.save(location)

                # 存储数据库路径
                details.logo = location
                details.save()
            except:
                details.save()

            # 关联我们当前这本书的详细信息
            book_obj = Book.objects.get(id=int(request.POST.get("book_id")))
            # 如果book_obj是一个空的字符串，那么book_obj这里会报错
            book_obj.info = details
            book_obj.save()

            ret['status'] = 'success'
            ret['data'] = '图书信息完善成功'

            return JsonResponse(ret)
        else:
            ret['data'] = details_form.errors

            return JsonResponse(ret)


class Book_Del(View):
    """
    书籍删除功能
    """

    def post(self, request):
        ret = {'status': "success", "data": "删除成功"}

        book_id = request.POST.get('book_id')
        book_id = int(book_id)

        book_obj = Book.objects.get(id=book_id)
        book_obj.delete()

        return JsonResponse(ret)


class Edit_Book(View):

    def get(self, request, book_id):
        """
        回显数据
        book_id    managerbook/urls 中已经定义了book_id的分组命名，所以可以直接拿到。
        :return:
        """

        author_id = []
        book_id = int(book_id)
        book = Book.objects.get(id=book_id)
        book_dict = model_to_dict(book)

        author_list = book_dict['author']
        for author_obj in author_list:  # 'author': <QuerySet [<Author: 作者1>, <Author: 作者2>]>
            author_id.append(author_obj.id)  # 转成字典 'author': [<Author: 作者1>, <Author: 作者2>]
            # 才是真正的字典

        # print(book_dict)      #initial需要一个字典，所以用 model_to_dict处理
        # 多对多的时候会出问题，比如多个作者

        try:
            details = Details.objects.get(id=book_dict['info'])
            details_dict = model_to_dict(details)
            details_form = DetailsForm(initial=details_dict)
        except:
            details = None
            details_form = DetailsForm()

        book_dict['author'] = author_id
        book_form = BookForm(initial=book_dict)

        return render(request, 'book_edit.html', {
            'book_form': book_form,
            'details_form': details_form,
            'book_id': book_id,
            'details': details,
        })

        # book_form = BookForm(initial=)
        # details_form = DetailsForm(initial=)

    def post(self, request,book_id):
        """
        提交更改数据
            几种更新：
            1.带图片更新已有的书籍详情信息　（替换已有的图片）
            2.不带图片更新已有的书籍详情信息 （新上传一个图片）
                (1) 更新已有的书籍详情信息(try捕捉错误处理图片)
            3.没有创建图书详情信息  (创建一个图书详情信息，上传图片)
            4.没有创建图书详情信息且不上传图片的 (创建一个图书详情信息，不上传图片)
                (2) 创建图书详情信息(try捕捉错误处理图片)
        更新流程：
            1.获取用户提交POST值并且传入我们的表单
            2.双表单的验证 book_form.is_valid()=True and details_form.is_valid()==True
            3.更新(4种情况)
        :param request:
        :return:
        """
        details_form = DetailsForm(request.POST, request.FILES)
        book_form = BookForm(request.POST)

        if details_form.is_valid() and book_form.is_valid():
            """
            双表单的验证
            """
            book_data = book_form.cleaned_data
            details_data = details_form.cleaned_data

            """拿到book queryset要进行update"""
            book = Book.objects.filter(id=int(book_id))

            try:
                """拿到这本书的详情信息，如果执行try里面的代码，
                就代表要更新详情信息，如果执行except就是创建详情信息
                """
                #需要对象，给列表，就需要用list[0]去取对象，否则就直接用对象名就可以
                details = Details.objects.filter(id=int(book[0].info_id))
            except:
                details = None

            """对book进行update更新"""
            book.update(
                name=book_data['name'],
                publish_year=book_data['publish_year'],
                price=book_data['price'],
                stocks=book_data['stocks'],
                status=book_data['status'],
                type_id=book_data['type'],
                publisher_id=book_data['publisher'],
            )

            # 多对多作者更新处理
            book[0].author.set(book_data['author'])

            print('book更新成功')

            if details:
                """
                更新书籍详情信息
                """
                try:
                    """
                    如果执行try里面的代码，就代表要更新图片，
                    反之执行except里面的代码，就代表不更新图片。
                    """
                    # 图片处理
                    logo = request.FILES['logo']
                    location = 'media/images/logos/' + \
                               str(details_data['words']) + str(details_data['pages']) + '_' + str(logo.name)
                    img = Image.open(logo)
                    img.save(location)

                    details.update(
                        chapter=details_data['chapter'],
                        contentinfo=details_data['contentinfo'],
                        catalog=details_data['catalog'],
                        words=details_data['words'],
                        pages=details_data['pages'],
                        logo=location
                    )
                except:
                    details.update(
                        chapter=details_data['chapter'],
                        contentinfo=details_data['contentinfo'],
                        catalog=details_data['catalog'],
                        words=details_data['words'],
                        pages=details_data['pages'],
                    )

                return render(request, 'book_edit.html', {
                    'book_form': book_form,
                    'details_form': details_form,
                    'details': details[0],
                    'book_id': book_id,
                })
            else:
                """
                创建书籍详情信息
                """
                # 实例化一个Details对象，用于后面的创建保存
                details = Details()

                # 拿到当前这本书的book对象，用于后面的详情信息与书籍绑定
                book_obj = Book.objects.get(id=int(book_id))

                try:
                    """
                    如果执行try里面的代码，
                    创建一条details记录，
                    同时要绑定到当前这本书(把这个书籍详情信息对应到这本书上)，

                    反之如果执行except里面的代码，
                    创建一条不带图片的details记录，
                    同时要绑定到当前这本书(把这个书籍详情信息对应到这本书上)，
                    """
                    # 处理图片
                    logo = request.FILES['logo']
                    location = 'media/images/logos/' + \
                               str(details_data['words']) + str(details_data['pages']) + '_' + str(logo.name)
                    img = Image.open(logo)
                    img.save(location)

                    details.chapter = details_data['chapter']
                    details.contentinfo = details_data['contentinfo']
                    details.catalog = details_data['catalog']
                    details.words = details_data['words']
                    details.pages = details_data['pages']
                    details.logo = location
                    details.save()

                    book_obj.info = details
                    book_obj.save()
                except:

                    details.chapter = details_data['chapter']
                    details.contentinfo = details_data['contentinfo']
                    details.catalog = details_data['catalog']
                    details.words = details_data['words']
                    details.pages = details_data['pages']
                    details.save()

                    book_obj.info = details          #绑定关系
                    book_obj.save()

            return render(request, 'book_edit.html', {
                'book_form': book_form,
                'details_form': details_form,
                'details': details,
                'book_id': book_id,
            })

# class index(View):
#
#     def get(self,request):
#
#         book_obj = Book.objects.all()
#
#         return  render(request,'book.html',{
#             'book_obj':book_obj
#         })

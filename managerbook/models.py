from django.db import models

# Create your models here.

class Book(models.Model):

    name = models.CharField(max_length=32,verbose_name="图书名")
    publish_year = models.DateField(verbose_name="图书出版时间")
    publish_add = models.DateTimeField(verbose_name="图书添加时间",auto_now_add=True)
    price = models.IntegerField(verbose_name="图书价格")
    stocks = models.IntegerField(verbose_name="图书库存")
    status = models.BooleanField(verbose_name="出版状态,0未出版，1出版",default=True)
    type = models.ForeignKey("TypeBook")
    author = models.ManyToManyField("Author")
    publisher = models.ForeignKey("Publisher")
    info = models.OneToOneField("Details",blank=True,null=True,unique=True)

    def __str__(self):

        return self.name

class TypeBook(models.Model):

    type_book = models.CharField(max_length=32,verbose_name="图书类型")

    def __str__(self):

        return self.type_book

class Author(models.Model):

    name = models.CharField(max_length=32,verbose_name="作者名")
    address = models.CharField(max_length=32,verbose_name="作者所在地")
    phone = models.CharField(max_length=11,verbose_name="作者联系电话")
    email = models.EmailField(verbose_name="作者联系邮箱")
    authorinfo = models.TextField(verbose_name="作者简介")

    def __str__(self):

        return self.name


class Publisher(models.Model):

    name = models.CharField(max_length=32,verbose_name="出版社名")
    address = models.CharField(max_length=32,verbose_name="出版社地址")

    def __str__(self):

        return self.name

class Details(models.Model):

    chapter = models.CharField(max_length=32,verbose_name="章节")
    pages = models.IntegerField(verbose_name="页数")
    words = models.IntegerField(verbose_name="字数")
    contentinfo = models.TextField(verbose_name="内容简介")
    logo = models.ImageField(verbose_name="图书封面",max_length=100)
    catalog = models.TextField(verbose_name="目录")
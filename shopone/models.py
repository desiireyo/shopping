from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate,logout

# Create your models here.
class Setgroup(models.Model):
    code=models.CharField(max_length=255,null=False)
    name=models.CharField(max_length=255,null=False)
    slug=models.SlugField(max_length=255,unique=True,null=False)

    def __str__(self):
        return self.name
    
    def get_url(self):
       return reverse('product_by_group',args=[self.slug])

class Setsubgroup(models.Model):
    code=models.CharField(max_length=255,null=False)
    name=models.CharField(max_length=255,null=False)
    slug=models.SlugField(max_length=255,unique=True,null=False)
    group=models.ForeignKey(Setgroup,on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    def get_url(self):
       return reverse('product_by_subgroup',args=[self.group.slug,self.slug])

class Settypegroup(models.Model):
    code=models.CharField(max_length=255,null=False)
    name=models.CharField(max_length=255,null=False)
    slug=models.SlugField(max_length=255,unique=True,null=False)
    subgroup=models.ForeignKey(Setsubgroup,on_delete=models.PROTECT)
    group=models.ForeignKey(Setgroup,on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    def get_url(self):
       return reverse('product_by_typegroup',args=[self.group.slug,self.subgroup.slug,self.slug])

class Setunit(models.Model):
    code=models.CharField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,unique=True)

    def __str__(self):
        return self.name

class Setstatus(models.Model):
    code=models.CharField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    code=models.CharField(max_length=100)
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,unique=True)
    barcode=models.CharField(max_length=255,unique=True)
    productname=models.TextField(blank=True)
    price_mem=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    disct_mem=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    typdisct_mem=models.BooleanField(default=True)
    netprice_mem=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    price_guest=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    disct_guest=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    typdisct_guest=models.BooleanField(default=True)
    netprice_guest=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    group=models.ForeignKey(Setgroup,on_delete=models.PROTECT)
    subgroup=models.ForeignKey(Setsubgroup,on_delete=models.PROTECT)
    typegroup=models.ForeignKey(Settypegroup,on_delete=models.PROTECT)
    unit=models.ForeignKey(Setunit,on_delete=models.PROTECT)
    status=models.ForeignKey(Setstatus,on_delete=models.PROTECT,default=1)
    stat_promotion=models.CharField(max_length=255,default='')
    flag_promotion=models.CharField(max_length=255,default='normal')
    image=models.ImageField(upload_to="product",blank=True)
    stock=models.IntegerField(default=0)
    available=models.BooleanField(default=True)
    memo=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product_detail',args=[self.group.slug,self.subgroup.slug,self.typegroup.slug,self.slug])

class ProductImageItem(models.Model):
    name=models.CharField(max_length=255)
    slug=models.ForeignKey(Product,on_delete=models.PROTECT)
    image=models.ImageField(upload_to="product",blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_id=models.CharField(max_length=255,blank=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    class Meta:
        db_table='cart'
        ordering=('created',)

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    statusBuy=models.CharField(max_length=100,default='ขาย')
    quantity=models.IntegerField()
    price_mem=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    active=models.BooleanField(default=True)

    class Meta:
        db_table='cartItem'
    
    def sub_total(self):
        sum_CartItem = self.product.netprice_mem * self.quantity
        return sum_CartItem

    def sub_total_guest(self):
        sum_CartItem = self.product.netprice_guest * self.quantity
        return sum_CartItem
    
    def __str__(self):
        return '%s %s' % (self.product.name, self.quantity)

class OrderGuest(models.Model):
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    tel=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    message=models.TextField(blank=True)
    flag=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='OrderGuest'

class OrderGuestItem(models.Model):
    order=models.ForeignKey(OrderGuest,on_delete=models.CASCADE)
    xproduct=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    flag=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='OrderGuestItem'
        ordering=('order',)

    def sub_total(self):
        return self.quantity*self.price
    
    def __str__(self):
        return self.product

class OrderMember(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    tel=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    message=models.TextField(blank=True)
    flag=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='OrderMember'
    
class OrderMemberItem(models.Model):
    order=models.ForeignKey(OrderMember,on_delete=models.CASCADE)
    xproduct=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    flag=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='OrderMemberItem'
        ordering=('order',)

    def sub_total(self):
        return self.quantity*self.price
    
    def __str__(self):
        return self.product

class Pagesetting(models.Model):
    pagename = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to="page_setting",blank=True)
    message = models.TextField(blank=True)
    slug = models.ForeignKey(Product,on_delete=models.PROTECT,blank=True,null=True)
    flag=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagename

class ProfileUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    tel = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class ShippingRange(models.Model):
    price1_range = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    price2_range = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    price=models.DecimalField(max_digits=10,decimal_places=2,null=False)
    flag=models.BooleanField(default=True)
    memo = models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.price


class OrderAllUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.PROTECT,blank=True,null=True)
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    tel=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    message=models.TextField(blank=True)
    flag=models.BooleanField(default=False)
    status=models.CharField(max_length=255)
    dtcreated=models.DateField(auto_now_add=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='OrderAllUser'
    
class OrderAllUserItem(models.Model):
    order=models.ForeignKey(OrderAllUser,on_delete=models.PROTECT)
    xproduct=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    flag=models.BooleanField(default=False)
    statusBuy=models.CharField(max_length=100,default='ขาย')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='OrderAllUserItem'
        ordering=('order',)

    def sub_total(self):
        return self.quantity*self.price
    
    

class SetConditions(models.Model):
    orderNo=models.IntegerField()
    header=models.CharField(max_length=255)
    detail=models.TextField(blank=True)
    typedetail=models.CharField(max_length=100)
    flag=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.header

class setProducttoPromotion(models.Model):
    barcode = models.ForeignKey(Product,on_delete=models.PROTECT)
    proname = models.CharField(max_length=255)
    quantity = models.IntegerField()
    free = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    fdate=models.DateField()
    ldate=models.DateField()
    flag=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.proname

class setContact(models.Model):
    company_name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    Phone = models.CharField(max_length=100)
    Phone1 = models.CharField(max_length=100)
    Phone2 = models.CharField(max_length=100)
    line_id = models.CharField(max_length=100)
    line_link = models.CharField(max_length=100)
    line_qrcode = models.ImageField(upload_to="contact",blank=True)
    email = models.CharField(max_length=100)
    time_openshop=models.DateField()
    time_closeshop=models.DateField()
    time_openoffice=models.DateField()
    time_closeoffice=models.DateField()
    facebook_link = models.CharField(max_length=255)
    pic_contact1 = models.ImageField(upload_to="contact",blank=True)
    pic_contact2 = models.ImageField(upload_to="contact",blank=True)
    time_openshop=models.DateField()
    time_closeshop=models.DateField()
    time_openoffice=models.DateField()
    time_closeoffice=models.DateField()

    def __str__(self):
        return self.company_name
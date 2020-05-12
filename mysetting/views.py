from django.shortcuts import render, get_object_or_404, redirect
from shopone.models import Setgroup,Setsubgroup,Settypegroup,Setstatus,Setunit,Product,ProductImageItem,Pagesetting
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from mysetting.forms import *
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import FileFieldForm,PicItemForm
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , authenticate,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum
from django.utils.decorators import method_decorator
from django.db.models import Q
import datetime

# Create your views here.
@login_required(login_url='Login')
def mysetting(request):    
    data1=OrderAllUser.objects.filter(status='member',flag=True).count()
    data2=OrderAllUser.objects.filter(status='member').count()
    data3=OrderAllUser.objects.filter(status='guest',flag=True).count()
    data4=OrderAllUser.objects.filter(status='guest').count()
    year = 2020
    month = 4
    data5=OrderAllUser.objects.filter(created__year__gte=year,created__month__gte=month,created__year__lte=year,created__month__lte=month).count()

    data6 = OrderAllUserItem.objects.values('xproduct').order_by('xproduct').annotate(total_qty=Sum('quantity'))
    data7=OrderAllUserItem.objects.select_related('xproduct').order_by('-created')
    data8 = OrderAllUserItem.objects.filter().values('xproduct').annotate(total_qty=Sum('quantity'))
    #User.objects.filter(user_type=type).values('id').annotate(total_time=Sum(useraction__time))
    context ={
        'data1' : data1,
        'data2' : data2,
        'data3' : data3,
        'data4' : data4,
        'data5' : data5,
        'data6' : data6,
        'data7' : data7,
        'data8' : data8,
    }
    return render(request,'mydashboard/index.html',context)

@login_required(login_url='Login')
def mysetgroup(request):
    datas = Setgroup.objects.all().order_by('id')
    context = {
        'datas': datas
    }
    return render(request,'mysetgroup/setgroup.html',context)

@login_required(login_url='Login')
def createSetgroup(request):
    return render(request,'mysetgroup/create.html')

@login_required(login_url='Login')
def addSetgroup(request):
    code = request.POST['code']
    name = request.POST['name']
    #slug = request.POST['slug']
    idLast = Setgroup.objects.filter().order_by('-id')[0]
    slug = 'G'+code+str(idLast.id)

    setgroup = Setgroup.objects.create(
        code = code,
        name = name,
        slug = slug,
    )
    setgroup.save()

    return redirect('mysetgroup')

@login_required(login_url='Login')
def editSetgroup(request,group_id=None):
    setgroup = Setgroup.objects.get(id=group_id)
    context = {
        'setgroup': setgroup
    }
    return render(request,'mysetgroup/update.html',context)

@login_required(login_url='Login')
def updSetgroup(request):
    group_id = request.POST['setgroup_id']
    code = request.POST['code']
    name = request.POST['name']
    #slug = request.POST['slug']
    

    try:
        updSetgroup=Setgroup.objects.get(id=group_id)
        # saveSetgroup=Setgroup()
        updSetgroup.code=code
        updSetgroup.name=name
        updSetgroup.save()
    except Setgroup.DoesNotExist:
        setgroup = Setgroup.objects.create(
            code = code,
            name = name,
        )
        setgroup.save()
    
    return redirect('mysetgroup')

@login_required(login_url='Login')
def delSetgroup(request,group_id=None):
    setgroup = Setgroup.objects.get(id=group_id)    
    setgroup.delete()

    return redirect('mysetgroup')

class SetsubgroupListView(ListView):
    model = Setsubgroup
    template_name = 'mysetsubgroup/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SetsubgroupCreateView(CreateView):
    model = Setsubgroup
    template_name = 'mysetsubgroup/create.html'
    form_class = SetsubgroupForm
    success_url = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(SetsubgroupCreateView, self).get_context_data(**kwargs)
        context["form_setsubgroup"] = SetsubgroupForm()
        return context

    def post(self, request, *args, **kwargs):
        form_setgroup = SetsubgroupForm(request.POST)
        if form_setgroup.is_valid():
            return self.form_valid(form_setgroup)

    def form_valid(self, form):
        self.object = form.save()
        return super(SetsubgroupCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mysetsubgroup')

class SetsubgroupUpdateView(UpdateView):
    model = Setsubgroup
    template_name = 'mysetsubgroup/create.html'
    form_class = SetsubgroupForm
    success_url = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SetsubgroupUpdateView, self).get_context_data(**kwargs)
        context["form_setsubgroup"] = SetsubgroupForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_setsubgroup = SetsubgroupForm(request.POST, instance=self.object)
        if form_setsubgroup.is_valid():
            return self.form_valid(form_setsubgroup)

    def form_valid(self, form):
        self.object = form.save()
        return super(SetsubgroupUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mysetsubgroup')

@login_required(login_url='Login')
def SetsubgroupDeleteView(request,group_id=None):
    setsubgroup = Setsubgroup.objects.get(id=group_id)    
    setsubgroup.delete()

    return redirect('mysetsubgroup')

@login_required(login_url='Login')
def mysettypegroup(request):
    datas = Settypegroup.objects.all().order_by('id')
    queryset = Settypegroup.objects.select_related('group','subgroup').order_by('-code')
    
    context = {
        'datas': datas,
        'queryset': queryset,
    }
    return render(request,'mysettypegroup/index.html',context)

@login_required(login_url='Login')
def createSettypegroup(request):
    data1 = Setgroup.objects.all().order_by('code')
    data2 = Setsubgroup.objects.all().order_by('code')
    context = {
        'data1': data1,
        'data2': data2,
    }
    return render(request,'mysettypegroup/create.html',context)

@login_required(login_url='Login')
def addSettypegroup(request):
    if request.method=='POST':
        code = request.POST['code']
        name = request.POST['name']
        #slug = request.POST['slug']
        group = request.POST['group']
        subgroup = request.POST['subgroup']
        
        setgroup = Setgroup.objects.get(id=group)
        setsubgroup = Setsubgroup.objects.get(id=subgroup)
        idLast = Settypegroup.objects.filter().order_by('-id')[0]
        slug = 'T-'+str(setgroup.code)+str(setsubgroup.code)+str(idLast.id)

        settypegroup = Settypegroup.objects.create(
            code = code,
            name = name,
            slug = slug,
            group_id = group,
            subgroup_id = subgroup
        )
        settypegroup.save()

    return redirect('mysettypegroup')

@login_required(login_url='Login')
def editSettypegroup(request,settypegroup_id=None):    
    settypegroup = Settypegroup.objects.get(id=settypegroup_id)
    setgroup = Setgroup.objects.get(id=settypegroup.group_id)
    setsubgroup = Setsubgroup.objects.get(id=settypegroup.subgroup_id)

    data1 = Setgroup.objects.all().order_by('code')
    data2 = Setsubgroup.objects.filter(group_id=settypegroup.group_id).order_by('code')

    # data2 = Setsubgroup.objects.filter(group_id=product.group_id).order_by('code')
    # data3 = Settypegroup.objects.filter(subgroup_id=product.subgroup_id).order_by('code')

    context = {
        'data1': data1,
        'data2': data2,
        'settypegroup': settypegroup,
        'setgroup': setgroup,
        'setsubgroup': setsubgroup,
    }
    return render(request,'mysettypegroup/update.html',context)

@login_required(login_url='Login')
def updSettypegroup(request):
    if request.method=='POST':
        settypegroup_id = request.POST['settypegroup_id']
        code = request.POST['code']
        name = request.POST['name']
        #slug = request.POST['slug']
        group = request.POST['group']
        subgroup = request.POST['subgroup']

        try:
            updSettypegroup=Settypegroup.objects.get(id=settypegroup_id)
            # saveSetgroup=Setgroup()
            updSettypegroup.code=code
            updSettypegroup.name=name
            #updSettypegroup.slug=slug
            updSettypegroup.group_id=group
            updSettypegroup.subgroup_id=subgroup
            updSettypegroup.save()
        except Settypegroup.DoesNotExist:
            settypegroup = Settypegroup.objects.create(
                code = code,
                name = name,
                #slug = slug,
                group_id = group,
                subgroup_id = subgroup
            )
            settypegroup.save()
    
    return redirect('mysettypegroup')

@login_required(login_url='Login')
def delSettypegroup(request,settypegroup_id=None):
    settypegroup = Settypegroup.objects.get(id=settypegroup_id)    
    settypegroup.delete()

    return redirect('mysettypegroup')

@login_required(login_url='Login')
def myproduct(request):
    # datas = Product.objects.all().order_by('id')
    queryset = Product.objects.select_related('group','subgroup','typegroup','unit').order_by('-code')
    
    context = {        
        'queryset': queryset,
    }
    return render(request,'myproduct/index.html',context)

@login_required(login_url='Login')
def createProduct(request):
    data1 = Setgroup.objects.all().order_by('code')
    data2 = Setsubgroup.objects.all().order_by('code')
    data3 = Settypegroup.objects.all().order_by('code')
    data4 = Setunit.objects.all().order_by('code')
    data5 = Setstatus.objects.all().order_by('code')
    context = {
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
    }
    return render(request,'myproduct/create.html',context)

@login_required(login_url='Login')
def addProduct(request):
    if request.method=='POST':
        code = request.POST['code']
        name = request.POST['name']
        productname = request.POST['productname']
        barcode = request.POST['barcode']
        # slug = request.POST['slug']
        group = request.POST['group']
        subgroup = request.POST['subgroup']
        typegroup = request.POST['typegroup']
        unit = request.POST['unit']
        status = request.POST['status']
        price_mem = request.POST['price_mem']
        disct_mem = request.POST['disct_mem']
        netprice_mem = request.POST['netprice_mem']
        price_guest = request.POST['price_guest']
        disct_guest = request.POST['disct_mem']
        netprice_guest = request.POST['netprice_mem']
        # exampleInputFile = request.POST['exampleInputFile']
        memo = request.POST['memo']

        setgroup = Setgroup.objects.get(id=group)
        setsubgroup = Setsubgroup.objects.get(id=subgroup)
        settypegroup = Settypegroup.objects.get(id=typegroup)
        idProduct = Product.objects.filter().order_by('-id')[0]
        txt_slug = str(setgroup.code)+str(setsubgroup.code)+str(settypegroup.code)+str(idProduct.id)
        slug = txt_slug

        # myfile = request.FILES['exampleInputFile']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)

        # print(request.FILES['id_InputFile'])
        # myfile = request.FILES.get['id_InputFile']
        
        stock = 10
        if len(request.FILES) != 0:
            p = request.FILES['nm_InputFile']

            saveProduct=Product()
            saveProduct.code=code
            saveProduct.name=name
            saveProduct.productname=productname
            saveProduct.barcode=barcode
            saveProduct.slug=slug
            saveProduct.group_id=group
            saveProduct.subgroup_id=subgroup
            saveProduct.typegroup_id=typegroup
            saveProduct.unit_id=unit
            saveProduct.status_id=status
            saveProduct.price_mem=price_mem
            saveProduct.disct_mem=disct_mem
            saveProduct.netprice_mem=netprice_mem
            saveProduct.price_guest=price_guest
            saveProduct.disct_guest=disct_guest
            saveProduct.netprice_guest=netprice_guest
            saveProduct.stock=stock
            saveProduct.memo=memo

            saveProduct.image=p
            saveProduct.save()
        else :
            saveProduct=Product()
            saveProduct.code=code
            saveProduct.name=name
            saveProduct.productname=productname
            saveProduct.barcode=barcode
            saveProduct.slug=slug
            saveProduct.group_id=group
            saveProduct.subgroup_id=subgroup
            saveProduct.typegroup_id=typegroup
            saveProduct.unit_id=unit
            saveProduct.status_id=status
            saveProduct.price_mem=price_mem
            saveProduct.disct_mem=disct_mem
            saveProduct.netprice_mem=netprice_mem
            saveProduct.price_guest=price_guest
            saveProduct.disct_guest=disct_guest
            saveProduct.netprice_guest=netprice_guest
            saveProduct.stock=stock
            saveProduct.memo=memo
            saveProduct.save()

        

        # product = Product.objects.create(
        #     code = code,
        #     name = name,
        #     productname = productname,
        #     barcode = barcode,
        #     slug = slug,
        #     group_id = group,
        #     subgroup_id = subgroup,
        #     typegroup_id = typegroup,
        #     unit_id = unit,
        #     status_id = status,
        #     price_mem = price_mem,
        #     disct_mem = disct_mem,
        #     netprice_mem = netprice_mem,
        #     price_guest = price_guest,
        #     disct_guest = disct_guest,
        #     netprice_guest = netprice_guest,
        #     stock = 10,
        #     image = Product(image = p),
        #     memo = memo
        # )
        # product.save()

    return redirect('myproduct')

@login_required(login_url='Login')
def editProduct(request,product_id=None):
    data1 = Setgroup.objects.all().order_by('code')
    data4 = Setunit.objects.all().order_by('code')
    data5 = Setstatus.objects.all().order_by('code')

    product = Product.objects.get(id=product_id)
    settypegroup = Settypegroup.objects.get(id=product.typegroup_id)
    setgroup = Setgroup.objects.get(id=product.group_id)
    setsubgroup = Setsubgroup.objects.get(id=product.subgroup_id)
    setunit = Setunit.objects.get(id=product.unit_id)
    setstatus = Setstatus.objects.get(id=product.status_id)

    
    data2 = Setsubgroup.objects.filter(group_id=product.group_id).order_by('code')
    data3 = Settypegroup.objects.filter(subgroup_id=product.subgroup_id).order_by('code')

    context = {
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'product': product,
        'settypegroup': settypegroup,
        'setgroup': setgroup,
        'setsubgroup': setsubgroup,
        'setunit': setunit,
        'setstatus': setstatus
    }
    return render(request,'myproduct/update.html',context)

@login_required(login_url='Login')
def updProduct(request):
    if request.method=='POST':
        product_id = request.POST['product_id']
        code = request.POST['code']
        name = request.POST['name']
        productname = request.POST['productname']
        barcode = request.POST['barcode']
        slug = request.POST['slug']
        group = request.POST['group']
        subgroup = request.POST['subgroup']
        typegroup = request.POST['typegroup']
        unit = request.POST['unit']
        status = request.POST['status']
        price_mem = request.POST['price_mem']
        disct_mem = request.POST['disct_mem']
        netprice_mem = request.POST['netprice_mem']
        price_guest = request.POST['price_guest']
        disct_guest = request.POST['disct_mem']
        netprice_guest = request.POST['netprice_mem']
        # exampleInputFile = request.POST['exampleInputFile']
        memo = request.POST['memo']
        stock = 10

        setgroup = Setgroup.objects.get(id=group)
        setsubgroup = Setsubgroup.objects.get(id=subgroup)
        settypegroup = Settypegroup.objects.get(id=typegroup)
        # txt_slug = setgroup.code+setsubgroup.code+settypegroup.code
        # slug = txt_slug

        
        # filepath = request.FILES('exampleInputFile')
        
        if len(request.FILES) != 0:
            p = request.FILES['nm_InputFile']
            
            updproduct=Product.objects.get(id=product_id)
            updproduct.code=code
            updproduct.name=name
            updproduct.productname=productname
            updproduct.barcode=barcode
            updproduct.slug=slug
            updproduct.group_id=group
            updproduct.subgroup_id=subgroup
            updproduct.typegroup_id=typegroup
            updproduct.unit_id=unit
            updproduct.status_id=status
            updproduct.price_mem=price_mem
            updproduct.disct_mem=disct_mem
            updproduct.netprice_mem=netprice_mem
            updproduct.price_guest=price_guest
            updproduct.disct_guest=disct_guest
            updproduct.netprice_guest=netprice_guest
            updproduct.stock=stock
            updproduct.memo=memo
            updproduct.image=p

            updproduct.save()
        else :
            updproduct=Product.objects.get(id=product_id)
            updproduct.code=code
            updproduct.name=name
            updproduct.productname=productname
            updproduct.barcode=barcode
            updproduct.slug=slug
            updproduct.group_id=group
            updproduct.subgroup_id=subgroup
            updproduct.typegroup_id=typegroup
            updproduct.unit_id=unit
            updproduct.status_id=status
            updproduct.price_mem=price_mem
            updproduct.disct_mem=disct_mem
            updproduct.netprice_mem=netprice_mem
            updproduct.price_guest=price_guest
            updproduct.disct_guest=disct_guest
            updproduct.netprice_guest=netprice_guest
            updproduct.stock=stock
            updproduct.memo=memo

            updproduct.save()
        
    
    return redirect('myproduct')

@login_required(login_url='Login')
def delProduct(request,product_slug=None):
    product = Product.objects.get(slug=product_slug)    
    product.delete()

    return redirect('myproduct')

@login_required(login_url='Login')
def picproduct(request):
    # datas = Product.objects.all().order_by('id')
    queryset = ProductImageItem.objects.select_related('slug').order_by('-slug')
    # query2 = ProductImageItem.objects.get(slug_id=queryset.slug)
    
    context = {        
        'queryset': queryset,
        # 'query2': query2
    }
    return render(request,'picproduct/index.html',context)

@login_required(login_url='Login')
def createPicProduct(request):
    data1 = Product.objects.all().order_by('code')
    context = {
        'data1': data1,
    }
    return render(request,'picproduct/create.html',context)

@login_required(login_url='Login')
def addPicProduct(request):
    if request.method=='POST':        
        name = request.POST['name']        
        slug = request.POST['slug']
        # name = Product.objects.get(slug=slug)

        if len(request.FILES) != 0:
            # p = request.FILES['nm_InputFile']
            files = request.FILES.getlist('nm_InputFile')
            for f in files:

                saveProduct=ProductImageItem()
                saveProduct.name=name
                saveProduct.slug_id=slug
                saveProduct.image=f
                saveProduct.save()
            return redirect('picproduct')

    return render(request,'picproduct/create.html')

@login_required(login_url='Login')
def editProductImage(request,productimage_id=None):
    data1 = Product.objects.all().order_by('id')
    productitem = ProductImageItem.objects.get(id=productimage_id)    
    cur_product = Product.objects.get(id=productitem.slug_id)

    context = {
        'data1': data1,
        'productitem': productitem,
        'cur_product': cur_product,
    }
    return render(request,'picproduct/update.html',context)

@login_required(login_url='Login')
def updProductImg(request):
    if request.method=='POST':
        productimg_id = request.POST['productimg_id']
        name = request.POST['name']
        slug = request.POST['slug']
        slug = Product.objects.get(id=slug)

        if len(request.FILES) != 0:
            p = request.FILES['nm_InputFile']
            
            updproductimg=ProductImageItem.objects.get(id=productimg_id)
            updproductimg.name=name
            updproductimg.slug=slug
            updproductimg.image=p

            updproductimg.save()
        else :
            updproductimg=ProductImageItem.objects.get(id=productimg_id)
            updproductimg.name=name
            updproductimg.slug=slug

            updproductimg.save()        

    return redirect('picproduct')

@login_required(login_url='Login')
def delProductImg(request,productimg_id=None):
    productimg = ProductImageItem.objects.get(id=productimg_id)    
    productimg.delete()

    return redirect('picproduct')

@login_required(login_url='Login')
def myOrdermember(request):
    # datas = Product.objects.all().order_by('id')
    queryset = OrderMember.objects.select_related('user').order_by('-user')
    query2 = OrderAllUserItem.objects.select_related('xproduct').order_by('-created')
    
    context = {        
        'queryset': queryset,
        'query2': query2,
    }
    return render(request,'myorder/index.html',context)

@login_required(login_url='Login')
def myOrderall(request):
    queryset = ''
    query2 = ''
    queryset_all =''
    query2_all = ''
    if request.method == "GET":
        allmember = request.GET.get('allmember')
        if not allmember:
            allmember = '0'
        allstat = request.GET.get('allstat')
        if not allstat:
            allstat = '0'

        query2 = OrderAllUserItem.objects.select_related('xproduct').order_by('created')
        if allmember == '2':
            if allstat == '0':
                queryset = OrderAllUser.objects.filter(status='member').select_related('user').order_by('-user')
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(status='member',flag=True).select_related('user').order_by('-user')
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(status='member',flag=False).select_related('user').order_by('-user')

        elif allmember == '1':
            if allstat == '0':
                queryset = OrderAllUser.objects.filter(status='guest').order_by('-created')
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(status='guest',flag=True).order_by('-created')
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(status='guest',flag=False).order_by('-created')
        
        elif allmember == '0' :
            if allstat == '0':
                queryset = OrderAllUser.objects.filter().order_by('-created')
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(flag=True).order_by('-created')
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(flag=False).order_by('-created')
    
    context = {        
        'queryset': queryset,
        'query2': query2,
        'allmember': allmember,
        'allstat': allstat,
        'queryset_all': queryset_all,
        'query2_all': query2_all,
    }

    return render(request,'myorder/index.html',context)

@login_required(login_url='Login')
def confirmOrdermember(request,order_id):
    if request.user.is_authenticated:
        order = OrderAllUser.objects.get(id=order_id)  
        order.flag=1

        order.save()
        
    return redirect('myOrderall')

@login_required(login_url='Login')
def CanconfirmOrdermember(request,order_id):
    if request.user.is_authenticated:
        order = OrderAllUser.objects.get(id=order_id)  
        order.flag=0

        order.save()
        
    return redirect('myOrderall')

@login_required(login_url='Login')
def myOrderguest(request):
    # datas = Product.objects.all().order_by('id')
    queryset = OrderGuest.objects.all().order_by('-created')
    query2 = OrderAllUserItem.objects.select_related('xproduct').order_by('-created')
    
    context = {        
        'queryset': queryset,
        'query2': query2
    }
    return render(request,'myorderguest/index.html',context)

@login_required(login_url='Login')
def confirmOrderguest(request,order_id):
    if request.user.is_authenticated:
        order = OrderAllUser.objects.get(id=order_id)  
        order.flag=1

        order.save()
        
    return redirect('myOrderall')

@login_required(login_url='Login')
def CanconfirmOrderguest(request,order_id):
    if request.user.is_authenticated:
        order = OrderAllUser.objects.get(id=order_id)  
        order.flag=0

        order.save()
        
    return redirect('myOrderall')

def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required(login_url='Login')
def rp_myorder(request):
    
    queryset = ''
    context = {}

    for_all = request.GET.get("for_all")
    allstat = request.GET.get("allstat")
    date1 = request.GET.get("date1")
    date2 = request.GET.get("date2")
    
    name = request.GET.get("name")
    if not for_all:
        for_all = '0'
    if not allstat:
        allstat = '0'
    if not name:
        name = ''

    # print(date1)
    if is_valid_queryparam(date1) and is_valid_queryparam(date2):
        # print('date1 11111111111:')
        context['date1'] = date1
        context['date2'] = date2
        
        if for_all == '0':            
            if allstat == '0':
                queryset = OrderAllUser.objects.filter(fname__icontains=name,dtcreated__range=(date1, date2)).order_by('-user')                
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(fname__icontains=name,flag=True,dtcreated__range=(date1, date2)).order_by('-user')                
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(fname__icontains=name,flag=False,dtcreated__range=(date1, date2)).order_by('-user')
                
        elif for_all == '1':
            if allstat == '0':
                queryset = OrderAllUser.objects.filter(status='guest',fname__icontains=name,created__range=(date1, date2)).order_by('-user')
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(status='guest',fname__icontains=name,flag=True,created__range=(date1, date2)).order_by('-user')
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(status='guest',fname__icontains=name,flag=False,created__range=(date1, date2)).order_by('-user')

        elif for_all == '2':
            if allstat == '0':
                queryset = OrderAllUser.objects.filter(status='member',fname__icontains=name,created__range=(date1, date2)).select_related('user').order_by('-user')
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(status='member',fname__icontains=name,flag=True,created__range=(date1, date2)).select_related('user').order_by('-user')
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(status='member',fname__icontains=name,flag=False,created__range=(date1, date2)).select_related('user').order_by('-user')
    else:
        
        if for_all == '0':
            if allstat == '0':
                queryset = OrderAllUser.objects.filter(fname__icontains=name).order_by('-user')
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(fname__icontains=name,flag=True).order_by('-user')
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(fname__icontains=name,flag=False).order_by('-user')

        elif for_all == '1':
            if allstat == '0':
                queryset = OrderAllUser.objects.filter(status='guest',fname__icontains=name).order_by('-user')
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(status='guest',fname__icontains=name,flag=True).order_by('-user')
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(status='guest',fname__icontains=name,flag=False).order_by('-user')
        elif for_all == '2':
            if allstat == '0':
                queryset = OrderAllUser.objects.filter(status='member',fname__icontains=name).select_related('user').order_by('-user')
            elif allstat == '1':
                queryset = OrderAllUser.objects.filter(status='member',fname__icontains=name,flag=True).select_related('user').order_by('-user')
            elif allstat == '2':
                queryset = OrderAllUser.objects.filter(status='member',fname__icontains=name,flag=False).select_related('user').order_by('-user')


    # print(for_mem)
    context['queryset'] = queryset
    context['for_all'] = for_all
    context['allstat'] = allstat
    context['name'] = name
    
    return render(request,'myreport/rp_myorder.html',context)

@login_required(login_url='Login')
def mysetunit(request):
    datas = Setunit.objects.all().order_by('id')
    context = {
        'datas': datas
    }
    return render(request,'mysetunit/index.html',context)

@login_required(login_url='Login')
def createSetunit(request):
    return render(request,'mysetunit/create.html')

@login_required(login_url='Login')
def addSetunit(request):
    code = request.POST['code']
    name = request.POST['name']
    slug = request.POST['slug']

    setunit = Setunit.objects.create(
        code = code,
        name = name,
        slug = slug
    )
    setunit.save()

    return redirect('mysetunit')

@login_required(login_url='Login')
def editSetunit(request,unit_id=None):
    setunit = Setunit.objects.get(id=unit_id)
    context = {
        'setunit': setunit
    }
    return render(request,'mysetunit/update.html',context)

@login_required(login_url='Login')
def updSetunit(request):
    unit_id = request.POST['setunit_id']
    code = request.POST['code']
    name = request.POST['name']
    slug = request.POST['slug']

    try:
        updSetunit=Setunit.objects.get(id=unit_id)
        # saveSetgroup=Setgroup()
        updSetunit.code=code
        updSetunit.name=name
        updSetunit.slug=slug
        updSetunit.save()
    except Setunit.DoesNotExist:
        setunit = Setunit.objects.create(
            code = code,
            name = name,
            slug = slug
        )
        setunit.save()
    
    return redirect('mysetunit')

@login_required(login_url='Login')
def delSetunit(request,unit_id=None):
    setunit = Setunit.objects.get(id=unit_id)    
    setunit.delete()

    return redirect('mysetunit')

@login_required(login_url='Login')
def mysetstatus(request):
    datas = Setstatus.objects.all().order_by('id')
    context = {
        'datas': datas
    }
    return render(request,'mysetstatus/index.html',context)

@login_required(login_url='Login')
def createSetstatus(request):
    return render(request,'mysetstatus/create.html')

@login_required(login_url='Login')
def addSetstatus(request):
    code = request.POST['code']
    name = request.POST['name']
    slug = request.POST['slug']

    setstatus = Setstatus.objects.create(
        code = code,
        name = name,
        slug = slug
    )
    setstatus.save()

    return redirect('mysetstatus')

@login_required(login_url='Login')
def editSetstatus(request,status_id=None):
    setstatus = Setstatus.objects.get(id=status_id)
    context = {
        'setstatus': setstatus
    }
    return render(request,'mysetstatus/update.html',context)

@login_required(login_url='Login')
def updSetstatus(request):
    status_id = request.POST['setstatus_id']
    code = request.POST['code']
    name = request.POST['name']
    slug = request.POST['slug']

    try:
        updSet=Setstatus.objects.get(id=status_id)
        # saveSetgroup=Setgroup()
        updSet.code=code
        updSet.name=name
        updSet.slug=slug
        updSet.save()
    except Setstatus.DoesNotExist:
        setstatus = Setstatus.objects.create(
            code = code,
            name = name,
            slug = slug
        )
        setstatus.save()
    
    return redirect('mysetstatus')

@login_required(login_url='Login')
def delSetstatus(request,status_id=None):
    setstatus = Setstatus.objects.get(id=status_id)    
    setstatus.delete()

    return redirect('mysetstatus')


def myDropdawn(request):
    context = {}
    groups = Setgroup.objects.all()
    subgroups = Setsubgroup.objects.all()
    typegroups = Settypegroup.objects.all()

    context['groups'] = groups
    context['subgroups'] = subgroups
    context['typegroups'] = typegroups

    return render(request,'myproduct/create.html',context)

def myDsubgroup(request):
    context = {}
    group = request.GET.get('group')
    subgroups = Setsubgroup.objects.filter(group_id=group)
    context['subgroups'] = subgroups

    return render(request,'includes/_Dsubgroup.html',context)

def myDtypegroup(request):
    context = {}
    subgroup = request.GET.get('subgroup')
    typegroups = Settypegroup.objects.filter(subgroup_id=subgroup)
    context['typegroups'] = typegroups

    return render(request,'includes/_Dtypegroup.html',context)


@login_required(login_url='Login')
def pagehomeSetting(request):    
    queryset = Pagesetting.objects.select_related('slug').filter(position='band').order_by('-slug')
    
    context = {        
        'queryset': queryset,
    }
    return render(request,'pagehomesetting/index.html',context)

@login_required(login_url='Login')
def createNewband(request):
    data1 = Product.objects.all().order_by('code')
    context = {
        'data1': data1,
    }
    return render(request,'pagehomesetting/create.html',context)

@login_required(login_url='Login')
def addNewband(request):
    if request.method=='POST':        
        pagename = request.POST['name']        
        message = request.POST['message']
        position = 'band'
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False
        

        if len(request.FILES) != 0:
            p = request.FILES['nm_InputFile']
            # files = request.FILES.getlist('nm_InputFile')            

            saveProduct=Pagesetting()
            saveProduct.pagename=pagename
            saveProduct.position=position
            saveProduct.message=message
            saveProduct.flag=flag
            
            saveProduct.image=p
            saveProduct.save()
        else :
            savePage=Pagesetting()
            savePage.pagename=pagename
            savePage.position=position
            
            savePage.message=message
            savePage.flag=flag
            savePage.save()
            
    return redirect('pagehomeSetting')

@login_required(login_url='Login')
def editBand(request,position_id=None):

    page = Pagesetting.objects.get(id=position_id)
    
    context = {        
        'page': page,
    }
    return render(request,'pagehomesetting/update.html',context)

@login_required(login_url='Login')
def updBand(request):
    if request.method=='POST':
        page_id = request.POST['page_id']
        pagename = request.POST['name']
        message = request.POST['message']
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False
        
        if len(request.FILES) != 0:
            p = request.FILES['nm_InputFile']
            
            updFunc=Pagesetting.objects.get(id=page_id)
            updFunc.pagename=pagename
            updFunc.message = message
            updFunc.image=p
            updFunc.flag=flag

            updFunc.save()
        else :
            updFunc=Pagesetting.objects.get(id=page_id)
            updFunc.pagename=pagename
            updFunc.message=message
            updFunc.flag=flag

            updFunc.save()        

    return redirect('pagehomeSetting')

@login_required(login_url='Login')
def delBand(request,position_id=None):
    page = Pagesetting.objects.get(id=position_id)    
    page.delete()

    return redirect('pagehomeSetting')

@login_required(login_url='Login')
def pagebestSell(request):
    queryset = Pagesetting.objects.select_related('slug').filter(position='best_sell').order_by('-slug')
    
    context = {        
        'queryset': queryset,
    }
    return render(request,'pagebestsell/index.html',context)

@login_required(login_url='Login')
def createNewbestsell(request):
    data1 = Product.objects.all().order_by('code')
    context = {
        'data1': data1,
    }
    return render(request,'pagebestsell/create.html',context)

@login_required(login_url='Login')
def addNewbestsell(request):
    if request.method=='POST':        
        # pagename = request.POST['name']        
        message = request.POST['message']
        slug = request.POST['slug']
        position = 'best_sell'
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False
        product = Product.objects.get(id=slug)
        pagename = product.code+' '+product.name

        saveProduct=Pagesetting()
        saveProduct.pagename=pagename
        saveProduct.position=position
        saveProduct.message=message
        saveProduct.slug_id=slug
        saveProduct.flag=flag
        saveProduct.save()
            
    return redirect('pagebestSell')

@login_required(login_url='Login')
def editBestsell(request,position_id=None):
    data1 = Product.objects.all().order_by('code')
    page = Pagesetting.objects.get(id=position_id)
    cur_product = Product.objects.get(id=page.slug_id)
    
    context = {        
        'page': page,
        'data1': data1,
        'cur_product': cur_product,
    }
    return render(request,'pagebestsell/update.html',context)

@login_required(login_url='Login')
def updBestsell(request):
    if request.method=='POST':
        page_id = request.POST['page_id']
        # pagename = request.POST['name']
        message = request.POST['message']
        slug = request.POST['slug']

        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False
        product = Product.objects.get(id=slug)
        pagename = product.code+' '+product.name
                
        updFunc=Pagesetting.objects.get(id=page_id)
        updFunc.pagename=pagename
        updFunc.message=message
        updFunc.slug_id=slug
        updFunc.flag = flag

        updFunc.save()        

    return redirect('pagebestSell')

@login_required(login_url='Login')
def delBestsell(request,position_id=None):
    page = Pagesetting.objects.get(id=position_id)    
    page.delete()

    return redirect('pagebestSell')

@login_required(login_url='Login')
def pagerecommend(request):
    queryset = Pagesetting.objects.select_related('slug').filter(position='recommend').order_by('-slug')
    
    context = {        
        'queryset': queryset,
    }
    return render(request,'pagerecommend/index.html',context)

@login_required(login_url='Login')
def createNewrecommand(request):
    data1 = Product.objects.all().order_by('code')
    context = {
        'data1': data1,
    }
    return render(request,'pagerecommend/create.html',context)

@login_required(login_url='Login')
def addNewrecommand(request):
    if request.method=='POST':        
        # pagename = request.POST['name']        
        message = request.POST['message']
        slug = request.POST['slug']
        
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False
        position = 'recommend'
        
        product = Product.objects.get(id=slug)
        pagename = product.code+' '+product.name

        saveProduct=Pagesetting()
        saveProduct.pagename=pagename
        saveProduct.position=position
        saveProduct.message=message
        saveProduct.slug_id=slug
        saveProduct.flag=flag
        saveProduct.save()
            
    return redirect('pagerecommend')

@login_required(login_url='Login')
def editRecommand(request,position_id=None):
    data1 = Product.objects.all().order_by('code')
    page = Pagesetting.objects.get(id=position_id)
    cur_product = Product.objects.get(id=page.slug_id)
    
    context = {        
        'page': page,
        'data1': data1,
        'cur_product': cur_product,
    }
    return render(request,'pagerecommend/update.html',context)

@login_required(login_url='Login')
def updRecommand(request):
    if request.method=='POST':
        page_id = request.POST['page_id']
        # pagename = request.POST['name']
        message = request.POST['message']
        slug = request.POST['slug']
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False

        product = Product.objects.get(id=slug)
        pagename = product.code+' '+product.name
                
        updFunc=Pagesetting.objects.get(id=page_id)
        updFunc.pagename=pagename
        updFunc.message=message
        updFunc.flag = flag
        updFunc.slug_id=slug

        updFunc.save()        

    return redirect('pagerecommend')

@login_required(login_url='Login')
def delRecommand(request,position_id=None):
    page = Pagesetting.objects.get(id=position_id)    
    page.delete()

    return redirect('pagerecommend')

@login_required(login_url='Login')
def pagepromotion(request):
    queryset = Pagesetting.objects.select_related('slug').filter(position='promotion').order_by('-slug')
    
    context = {        
        'queryset': queryset,
    }
    return render(request,'pagepromotion/index.html',context)

@login_required(login_url='Login')
def createNewpromotion(request):
    data1 = Product.objects.all().order_by('code')
    context = {
        'data1': data1,
    }
    return render(request,'pagepromotion/create.html',context)

@login_required(login_url='Login')
def addNewpromotion(request):
    if request.method=='POST':        
        # pagename = request.POST['name']        
        message = request.POST['message']
        slug = request.POST['slug']
        position = 'promotion'

        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False
        
        product = Product.objects.get(id=slug)
        pagename = product.code+' '+product.name

        saveProduct=Pagesetting()
        saveProduct.pagename=pagename
        saveProduct.position=position
        saveProduct.message=message
        saveProduct.slug_id=slug
        saveProduct.flag=flag
        saveProduct.save()
            
    return redirect('pagepromotion')

@login_required(login_url='Login')
def editPromotion(request,position_id=None):
    data1 = Product.objects.all().order_by('code')
    page = Pagesetting.objects.get(id=position_id)
    cur_product = Product.objects.get(id=page.slug_id)
    
    context = {        
        'page': page,
        'data1': data1,
        'cur_product': cur_product,
    }
    return render(request,'pagepromotion/update.html',context)

@login_required(login_url='Login')
def updPromotion(request):
    if request.method=='POST':
        page_id = request.POST['page_id']
        # pagename = request.POST['name']
        message = request.POST['message']
        slug = request.POST['slug']

        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False
        
        product = Product.objects.get(id=slug)
        pagename = product.code+' '+product.name
                
        updFunc=Pagesetting.objects.get(id=page_id)
        updFunc.pagename=pagename
        updFunc.message=message
        updFunc.slug_id=slug
        updFunc.flag=flag

        updFunc.save()        

    return redirect('pagepromotion')

@login_required(login_url='Login')
def delPromotion(request,position_id=None):
    page = Pagesetting.objects.get(id=position_id)    
    page.delete()

    return redirect('pagepromotion')

#กำหนดช่วงราคาขนส่ง
@login_required(login_url='Login')
def ShippingPrice(request):
    queryset = ShippingRange.objects.all().order_by('id')
    
    context = {        
        'queryset': queryset,
    }
    return render(request,'setshipping/index.html',context)

@login_required(login_url='Login')
def createShippingPrice(request):
    data1 = Product.objects.all().order_by('code')
    context = {
        'data1': data1,
    }
    return render(request,'setshipping/create.html',context)

@login_required(login_url='Login')
def addNewshipping(request):
    if request.method=='POST':        
        price1_range = request.POST['price1']
        price2_range = request.POST['price2']
        price = request.POST['price']
        message = request.POST['message']
        
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False

        saveApp=ShippingRange()
        saveApp.price1_range=price1_range
        saveApp.price2_range=price2_range
        saveApp.price=price
        saveApp.memo=message
        saveApp.flag=flag
        saveApp.save()
            
    return redirect('ShippingPrice')

@login_required(login_url='Login')
def editShipping(request,shipping_id=None):
    data1 = ShippingRange.objects.all().order_by('price1_range')
    page = ShippingRange.objects.get(id=shipping_id)
    # cur_product = Product.objects.get(id=page.slug_id)
    
    context = {
        'data1': data1,
        'page': page,
    }
    return render(request,'setshipping/update.html',context)

@login_required(login_url='Login')
def updShipping(request):
    if request.method=='POST':
        price1_range = request.POST['price1']
        price2_range = request.POST['price2']
        price = request.POST['price']
        message = request.POST['message']
        page_id = request.POST['page_id']
        
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False
                
        updFunc=ShippingRange.objects.get(id=page_id)
        updFunc.price1_range=price1_range
        updFunc.price2_range=price2_range
        updFunc.price = price
        updFunc.message=message
        updFunc.flag=flag

        updFunc.save()        

    return redirect('ShippingPrice')

@login_required(login_url='Login')
def delShipping(request,shipping_id=None):
    page = ShippingRange.objects.get(id=shipping_id)    
    page.delete()

    return redirect('ShippingPrice')

def SetCondition(request):
    queryset = SetConditions.objects.all().order_by('orderNo')

    context ={
        'queryset': queryset,
    }
    return render(request,'pageconditions/index.html',context)

def AddConditions(request):
    return render(request,'pageconditions/create.html')

def CreateConditions(request):
    if request.method=='POST':        
        orderNo = request.POST['order']
        header = request.POST['header']
        detail = request.POST['detail']
        typedetail = 'text'
        
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False

        saveApp=SetConditions()
        saveApp.orderNo=orderNo
        saveApp.header=header
        saveApp.detail=detail
        saveApp.typedetail=typedetail
        saveApp.flag=flag
        saveApp.save()
    return redirect('SetCondition')

def EditConditions(request,page_id=None):    
    data = SetConditions.objects.get(id=page_id)
        
    context = {
        'data': data,
    }
    return render(request,'pageconditions/update.html',context)

def UpdConditions(request):
    if request.method=='POST':        
        page_id = request.POST['page_id']
        orderNo = request.POST['order']
        header = request.POST['header']
        detail = request.POST['detail']
        typedetail = 'text'
        
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False

        updFunc=SetConditions.objects.get(id=page_id)
        updFunc.orderNo=orderNo
        updFunc.header=header
        updFunc.detail=detail
        updFunc.typedetail=typedetail
        updFunc.flag=flag
        updFunc.save()
    return redirect('SetCondition')

def DelConditions(request,page_id=None):
    page = SetConditions.objects.get(id=page_id)
    page.delete()

    return redirect('SetCondition')

def SetProducttoPromotion(request):
    queryset = setProducttoPromotion.objects.all().order_by('proname')

    context ={
        'queryset': queryset,
    }
    return render(request,'pagepromotion2/index.html',context)

def AddProducttoPromotion(request):
    queryset = Product.objects.all().order_by('group')

    context ={
        'queryset': queryset,
    }
    return render(request,'pagepromotion2/create.html',context)

def CreateProducttoPromotion(request):
    if request.method=='POST':        
        proname = request.POST['proname']
        slug = request.POST['slug']
        qty = request.POST['qty']
        free = request.POST['free']
        price = request.POST['price']
        fdate = request.POST['date1']
        ldate = request.POST['date2']
        
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False

        barcode = Product.objects.get(id=slug)

        saveApp=setProducttoPromotion()
        saveApp.proname=proname
        saveApp.barcode=barcode
        saveApp.quantity=qty
        saveApp.free=free
        saveApp.price=price
        saveApp.fdate=fdate
        saveApp.ldate=ldate
        saveApp.flag=flag
        saveApp.save()

        saveApp2=Product.objects.get(id=slug)
        saveApp2.stat_promotion=proname
        saveApp2.flag_promotion='promotion'
        saveApp2.save()
    return redirect('SetProducttoPromotion')

def EditPromotion2(request,page_id=None):    
    data = setProducttoPromotion.objects.get(id=page_id)
    queryset = Product.objects.all().order_by('group')

    cur_product = Product.objects.get(id=data.barcode_id)
        
    context = {
        'data': data,
        'queryset': queryset,
        'cur_product': cur_product,
    }
    return render(request,'pagepromotion2/update.html',context)

def UpdPromotion2(request):
    if request.method=='POST':
        page_id = request.POST['page_id']
        proname = request.POST['proname']
        slug = request.POST['slug']
        qty = request.POST['qty']
        free = request.POST['free']
        price = request.POST['price']
        fdate = request.POST['date1']
        ldate = request.POST['date2']
        
        if (request.POST['success'] == 'true'):
            flag = True
        else:
            flag = False

        barcode = Product.objects.get(id=slug)

        updFunc=setProducttoPromotion.objects.get(id=page_id)
        updFunc.proname=proname
        updFunc.barcode=barcode
        updFunc.quantity=qty
        updFunc.free=free
        updFunc.price=price
        updFunc.fdate=fdate
        updFunc.ldate=ldate
        updFunc.flag=flag
        updFunc.save()

        saveApp2=Product.objects.get(id=slug)
        saveApp2.stat_promotion=proname
        saveApp2.save()
    return redirect('SetProducttoPromotion')

def DelPromotion2(request,page_id=None):
    page = setProducttoPromotion.objects.get(id=page_id)
    page.delete()

    return redirect('SetProducttoPromotion')

def AddContact(request):
    queryset = Product.objects.all().order_by('group')

    context ={
        'queryset': queryset,
    }
    return render(request,'pagecontact/contact.html',context)

#######################################################################
#######################################################################
#######################################################################
class BasicUploadView(FormView):
    form_class = PicItemForm
    template_name = 'picproduct/create.html'  # Replace with your template.
    #success_url = '/picproduct'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # print(form.name)
        files = request.FILES.getlist('image')
        if form.is_valid():
            data = form.save(commit=False)
            print(data)
            for f in files:
                # form.image = f
                addpic = ProductImageItem(name='111', slug_id=10, image=f)
                addpic.save()
            return redirect('picproduct')
        else:
            return self.form_invalid(form)
#######################################################################
#######################################################################
#######################################################################
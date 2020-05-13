from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
from shopone.models import Product,Setgroup,Setsubgroup,Settypegroup,Setunit,Setstatus,ProductImageItem,Cart,CartItem,OrderGuest,OrderGuestItem,OrderMember,OrderMemberItem,Pagesetting,ProfileUser,ShippingRange,OrderAllUser,OrderAllUserItem,SetConditions,setProducttoPromotion,setContact,setWorktogether,setOurservice
from django.contrib.auth import login , authenticate,logout
from django.contrib.auth.models import Group,User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from . import forms
from shopone.forms import StateForm
import datetime,json
import math
from django.db.models import Avg, Count, Min, Sum


# Create your views here.
def index(request):
        
    data5 =[]
    data1 = Pagesetting.objects.all().filter(flag=True,position='best_sell')[:8]
    # data1 = OrderAllUserItem.objects.annotate(sku_count=Count('xproduct_id')).order_by('-sku_count')[:8]
    q1 = OrderAllUserItem.objects.values('xproduct','xproduct__id','xproduct__image').annotate(total_buy=Sum('quantity')).order_by('-total_buy')[:8]
    q2 = OrderAllUserItem.objects.values('xproduct').aggregate(sum_sale=Sum('quantity'))
    # print(q2)
    for txt in q1 :
        # print(txt)
        data5.append({'product': Product.objects.all().get(id=txt['xproduct__id']), 'total_buy' : txt['total_buy']})
    # print(data5)
    # xquery = Product.objects.filter(id=data1)
    # print(xquery)

    data2 = Pagesetting.objects.all().filter(flag=True,position='band')[:2]
    data3 = Pagesetting.objects.all().filter(flag=True,position='recommend')[:8]
    data4 = setProducttoPromotion.objects.all().filter(flag=True)[:8]
    # print(data4)
    
    
    # Pshipping = seshipping(total)
    context = UpdMinicart(request)
    context['datas1'] = q1
    context['data2'] = data2
    context['data3'] = data3
    context['data4'] = data4
    context['datas5'] = data5
    # print(data1.xproduct_id)
    # context['company'] = loadlayout(request)
    
    return render(request,'index.html',context)

def loadlayout(request):
    company = setContact.objects.get(id=1)
    context = {
        'company': company,
    }
    return render(request,'index.html',context)

def indexSetgroup(request,group_slug=None):
    products=None
    group_page=None

    if group_slug != None:
        group_page=get_object_or_404(Setgroup,slug=group_slug)
        products=Product.objects.all().filter(group=group_page,available=True)
    else :
        products=Product.objects.all().filter(available=True)
    
    context = UpdMinicart(request)
    context['products'] = products
    context['group'] = group_page
        
    return render(request,'shop.html',context)

def indexSetsubgroup(request,group_slug=None,subgroup_slug=None):
    products=None
    group_page=None
    subgroup_page=None

    if group_slug != None:
        group_page=get_object_or_404(Setgroup,slug=group_slug)
        subgroup_page=get_object_or_404(Setsubgroup,slug=subgroup_slug)
        products=Product.objects.all().filter(group=group_page,subgroup=subgroup_page,available=True)
    else :
        products=Product.objects.all().filter(available=True)
    
    context = UpdMinicart(request)
    context['products'] = products
    context['group'] = group_page
    context['subgroup'] = subgroup_page
        
    return render(request,'shop.html',context)

def indexSettypegroup(request,group_slug=None,subgroup_slug=None,typegroup_slug=None):
    products=None
    group_page=None
    subgroup_page=None
    typegroup_page=None

    if group_slug != None:
        group_page=get_object_or_404(Setgroup,slug=group_slug)
        subgroup_page=get_object_or_404(Setsubgroup,slug=subgroup_slug)
        typegroup_page=get_object_or_404(Settypegroup,slug=typegroup_slug)
        products=Product.objects.all().filter(group=group_page,subgroup=subgroup_page,typegroup=typegroup_page,available=True)
    else :
        products=Product.objects.all().filter(available=True)
    
    context = UpdMinicart(request)
    context['products'] = products
    context['group'] = group_page
    context['subgroup'] = subgroup_page    
    
    return render(request,'shop.html',context)

def shop(request):
    products = None
    products = Product.objects.all().filter(available=True)
    promotions = setProducttoPromotion.objects.all().filter(flag=True)

    #12 / 3 = 4
    paginator=Paginator(products,12)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try:
        productperPage=paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage=paginator.page(paginator.num_pages)

    context = UpdMinicart(request)
    context['products'] = products
    context['products'] = productperPage
    context['promotion'] = promotions
    
    return render(request,'shop.html',context)

def shop_promotion(request):
    products = None
    promotions = setProducttoPromotion.objects.all().filter(flag=True)
    products = Product.objects.all().filter(available=True,flag_promotion='promotion')


    #12 / 3 = 4
    paginator=Paginator(products,12)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try:
        productperPage=paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage=paginator.page(paginator.num_pages)

    context = UpdMinicart(request)
    context['products'] = products
    context['products'] = productperPage
    context['promotion'] = promotions
    
    return render(request,'shop_promotion.html',context)

def viewProduct(request,group_slug=None,subgroup_slug=None,typegroup_slug=None,product_slug=None):
    try:
        product=Product.objects.get(group__slug=group_slug,subgroup__slug=subgroup_slug,typegroup__slug=typegroup_slug,slug=product_slug)
        imageItems = ProductImageItem.objects.all().filter(slug__slug=product_slug)
        slug1 = Setgroup.objects.get(slug=group_slug)
        slug2 = Setsubgroup.objects.get(slug=subgroup_slug)
        slug3 = Settypegroup.objects.get(slug=typegroup_slug)
        product_related = Product.objects.filter(group__slug=group_slug,subgroup__slug=subgroup_slug,typegroup__slug=typegroup_slug)[:5]
        
        promotions = setProducttoPromotion.objects.all().filter(barcode__slug=product_slug)
        # promotion=get_object_or_404(setProducttoPromotion,barcode_id=product.id)
        # promotion = setProducttoPromotion.objects.get(id=10)
        # promotions = setProducttoPromotion.objects.select_related('barcode')

    except Exception as e :
        raise e

    context = UpdMinicart(request)
    context['product'] = product
    context['imageItems'] = imageItems
    context['slug1'] = slug1
    context['slug2'] = slug2
    context['slug3'] = slug3
    context['product_related'] = product_related
    context['promotion'] = promotions
       
    return render(request,'product.html',context)

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def addCart(request,product_id):
    product=Product.objects.get(id=product_id)
    context = {}

    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    
    # print("YYYYYY")
    # print(request.POST['product_qty'])
    
    try:
        #ซื้อรายการสินค้าซ้ำ
        cart_item=CartItem.objects.get(product=product,cart=cart)
        
        if request.method=='POST':
            qty = request.POST['product_qty']
            cart_item.quantity+=int(qty)
        else :
        #เปลี่ยนจำนวนรายการสินค้า
            cart_item.quantity+=1
        #บันทึก/อัพเดทค่า
        cart_item.save()
    except CartItem.DoesNotExist:
        #ซื้อรายการสินค้าครั้งแรก
        #บันทึกลงฐานข้อมูล
        if request.method=='POST':
            qty = request.POST['product_qty']
        else :
            qty = 1
        
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=qty
        )
        cart_item.save()

        # if product.stat_promotion != '':
        #     cart2_item=CartItem.objects.create(
        #         product=product,
        #         cart=cart,
        #         quantity=qty
        #     )
        #     cart2_item.save()

        # context['request'] = request.context
        
        context['data'] =cart_item

    return redirect(request.META['HTTP_REFERER'])
    # return render(request,'shop.html',context)
    # return redirect('shop')
    # return JsonResponse(context)

def addCart2(request):
    
    if request.method=='GET':
        product_id = request.GET['product_id']
        qty = request.GET['product_qty']

        product=Product.objects.get(id=product_id)
        if (product.stat_promotion) != '':
            
            proname = setProducttoPromotion.objects.get(barcode__id=product_id)
            print(proname)

        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
        
        try:
            #ซื้อรายการสินค้าซ้ำ
            cart_item=CartItem.objects.get(product=product,cart=cart)
            
            if request.method=='GET':
                qty = qty
                cart_item.quantity+=int(qty)
            else :
            #เปลี่ยนจำนวนรายการสินค้า
                cart_item.quantity+=1
            #บันทึก/อัพเดทค่า
            cart_item.save()
        except CartItem.DoesNotExist:
            #ซื้อรายการสินค้าครั้งแรก
            #บันทึกลงฐานข้อมูล
            if request.method=='GET':
                qty = qty
            else :
                qty = 1
            
            cart_item=CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=qty
            )
            cart_item.save()
        context = UpdMinicart(request)
        xx1 = context['cart_totalrow']
        # print(context['cart_totalrow'])
    
    # return JsonResponse({'cart_totalrow': xx1})
    return render(request, 'minicart.html', context)

def addCart3(request):
    print('addCart3')
    if request.method=='GET':
        product_id = request.GET['product_id']
        qty = request.GET['product_qty']

        product=Product.objects.get(id=product_id)
        
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
        
        try:
            #ซื้อรายการสินค้าซ้ำ
            cart_item=CartItem.objects.get(product=product,cart=cart,statusBuy='ขาย')
            
            if request.method=='GET':
                qty = qty
                cart_item.quantity+=int(qty)
            else :
            #เปลี่ยนจำนวนรายการสินค้า
                cart_item.quantity+=1
            #บันทึก/อัพเดทค่า
            cart_item.save()
        except CartItem.DoesNotExist:
            #ซื้อรายการสินค้าครั้งแรก
            #บันทึกลงฐานข้อมูล
            if request.method=='GET':
                qty = qty
            else :
                qty = 1
            
            cart_item=CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=qty
            )
            cart_item.save()

        ## check promotion ##
        if (product.stat_promotion) != '':
            pro = setProducttoPromotion.objects.get(barcode__id=product_id)
            print(pro.proname)
            cart_item=CartItem.objects.get(product=product,cart=cart,statusBuy='ขาย')

            if math.trunc(cart_item.quantity / pro.quantity) > 0:

                if (pro.free) == 0:
                    #cart_item=CartItem.objects.get(product=product,cart=cart,statusBuy='ขาย')
                    print(cart_item.quantity)
                    if cart_item.quantity >= pro.quantity:
                        print('pro XXXXXX')
                        decrease = math.trunc(cart_item.quantity / pro.quantity) * pro.price
                        try:
                            #ซื้อรายการสินค้าซ้ำ
                            cart_itemD=CartItem.objects.get(product=product,cart=cart,statusBuy='ลด')
                            
                            # cart_itemD.statusBuy='ลด',
                            cart_itemD.price_mem=decrease
                            cart_itemD.save()

                        except CartItem.DoesNotExist:
                            cart_itemD=CartItem.objects.create(
                                product=product,
                                cart=cart,
                                quantity=pro.free,
                                statusBuy='ลด',
                                price_mem=decrease
                            )
                            cart_itemD.save()
                else :
                
                    try:
                        #ซื้อรายการสินค้าซ้ำ
                        cart_itemP=CartItem.objects.get(product=product,cart=cart,statusBuy='แถม')
                                            
                        qty = int(math.trunc(cart_item.quantity / pro.quantity)) * int(pro.free)
                        cart_itemP.quantity=int(qty)
                        
                        cart_itemP.save()
                    except CartItem.DoesNotExist:
                        # print('GGGGG')
                        cart_itemP=CartItem.objects.create(
                            product=product,
                            cart=cart,
                            quantity= int(math.trunc(cart_item.quantity / pro.quantity)) * int(pro.free),
                            statusBuy='แถม'
                        )
                        cart_itemP.save()
                
            
        context = UpdMinicart(request)
        # xx1 = context['cart_totalrow']
        # print(context['cart_totalrow'])
    
    # return JsonResponse({'cart_totalrow': xx1})
    return render(request, 'minicart.html', context)

def UpdateCart(request):
    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for item in cart_items:
            cartItem=CartItem.objects.get(product=item.product,cart=cart)

            if request.method=='POST':
                xid = 'cart_qty'+item.product.id
                qty = request.POST['cart_qty']
            else :
                qty = 1
            
            cart_item=CartItem.objects.create(
                product=item.product,
                cart=item.cart,
                quantity=qty
            )
            cartItem.delete()
        cart_item.save()
    except Exception as e :
        pass
    
    return redirect('cartDetail')

def removeCart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    # typeD = CartItem.objects.get(product=product,cart=cart)
    # if (typeD.statusBuy) == 'ขาย':
    #     cartItem=CartItem.objects.get(product=product,cart=cart,statusBuy='ขาย')
    #     cartItem.delete()
    
    # if (typeD.statusBuy) == 'แถม':
    #     cartItemF=CartItem.objects.get(product=product,cart=cart,statusBuy='แถม')
    #     cartItemF.delete()

    # if (typeD.statusBuy) == 'ลด':
        # cartItemD=CartItem.objects.get(product=product,cart=cart,statusBuy='ลด')
        #ลบรายการสินค้า 1 ออกจากตะกร้า A โดยลบจาก รายการสินค้าในตะกร้า (CartItem)
                
        # cartItemD.delete()
    allCart = CartItem.objects.filter(cart=cart,product=product)
    for xx in allCart :
        xx.delete()
    

    return redirect('cartDetail')

def cartDetail(request):
    context = UpdMinicart(request)    
    
    return render(request,'cart.html',context)

def seshipping(xtotal=0):
    Pshipping = 0
    if xtotal > 0:
        shippingrange = ShippingRange.objects.filter(price1_range__lte=xtotal,price2_range__gte=xtotal)
        
        for shipping in shippingrange:
            Pshipping = shipping.price
    else:
        Pshipping=0
    
    return Pshipping

def checkout(request):
    context = UpdMinicart(request)
    if request.user.is_authenticated:
        user = ProfileUser.objects.get(user_id=request.user.id)
    else:
        user = ''
    context['user'] = user

    return render(request,'checkout.html',context)

def UpdMinicart(request):
    
    total=0
    counter=0
    counterF=0
    Pshipping = 0
    discount = 0
    cart_items=None
    cart_totalrow = None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลสินค้าในตะกร้า
        cart_totalrow=CartItem.objects.filter(cart=cart,active=True).count()
        
        for item in cart_items:
            if item.statusBuy == 'ขาย':
                if request.user.is_authenticated:
                    total+=(item.product.netprice_mem*item.quantity)
                else :
                    total+=(item.product.netprice_guest*item.quantity)
                counter+=item.quantity
            else:
                counterF+=item.quantity
                discount += item.price_mem

    except Exception as e :
        pass

    Pshipping=seshipping(total)
    totalall = (total + Pshipping) - discount
    
    context = {
        'cart_items': cart_items,
        'shipping' : Pshipping,
        'total': total,
        'totalall': totalall,
        'counter': counter,
        'cart_totalrow': cart_totalrow,
        'discount': discount,
    }
    return context

def addOrderGuest(request):
    total=0
    counter=0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.product.netprice_guest*item.quantity)
            counter+=item.quantity
    except Exception as e :
        pass

    if request.method=='POST':
        try :
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            tel = request.POST['tel']
            message = request.POST['message']

            order_guest = OrderAllUser.objects.create(
                fname = fname,
                lname = lname,
                email = email,
                tel = tel,
                message = message,
                total = total,
                status='guest',
            )
            order_guest.save()

            #บันทึกรายการสั่งซื้อ
            for item in cart_items :
                if item.statusBuy == 'ขาย':
                    xprice = item.product.netprice_guest
                elif item.statusBuy == 'แถม':
                    xprice = 0
                else:
                    xprice = item.price_mem

                order_guest_item=OrderAllUserItem.objects.create(
                    order=order_guest,
                    xproduct_id=item.product.id,
                    quantity=item.quantity,
                    price=xprice,
                )
                order_guest_item.save()
                #ลดจำนวน Stock
                # product=Opttran.objects.get(id=item.product.id)
                # product.stock=int(item.product.stock-order_item.quantity)
                # product.save()
                item.delete()
            return redirect('home')
        except Exception as e :
            pass
    
    return render(request,'checkout.html',dict(cart_items=cart_items,total=total,counter=counter))

def Register(request):
    context = {}
    if request.method=='POST':
        data = request.POST.copy()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        tel = request.POST['tel']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            saveRegist=User()
            saveRegist.username=email
            saveRegist.first_name=first_name
            saveRegist.last_name=last_name
            saveRegist.email=email
            saveRegist.tel=tel
            saveRegist.set_password(password)
            saveRegist.save()

            saveProfile=ProfileUser()
            saveProfile.user=User.objects.get(username=email)
            saveProfile.tel = tel
            saveProfile.save()

            new_user = authenticate(username=data.get('email'),
                                        password=data.get('password1'),
                                    )
            login(request, new_user)
        
        return redirect('orderHistory')
    context = UpdMinicart(request)

    return render(request,'register.html',context)

def addOrderMember(request):
    total=0
    counter=0
    cart_items=None
    xstatusBuy=''
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            if item.statusBuy == 'ขาย':
                total+=(item.product.netprice_mem*item.quantity)
                counter+=item.quantity
            elif item.statusBuy == 'แถม':
                total+=0
                counter+=item.quantity
            else:
                total+=((item.product.netprice_mem*item.quantity) - item.price_mem)
                counter+=item.quantity
    except Exception as e :
        pass

    # form = formChkout()

    if request.method=='POST':
        try :
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            tel = request.POST['tel']
            message = request.POST['message']
            user = request.POST['username']
            userX = request.user.id

            
            order_member = OrderAllUser.objects.create(
                fname = fname,
                lname = lname,
                email = email,
                tel = tel,
                message = message,
                total = total,
                user_id = userX,
                status = 'member'
            )
            order_member.save()


            #บันทึกรายการสั่งซื้อ
            for item in cart_items :
                if item.statusBuy == 'ขาย':
                    xprice = item.product.netprice_guest
                    xstatusBuy = 'ขาย'
                elif item.statusBuy == 'แถม':
                    xprice = 0
                    xstatusBuy = 'แถม'
                else:
                    xprice = item.price_mem
                    xstatusBuy = 'ลด'
                    
                order_member_item=OrderAllUserItem.objects.create(
                    order=order_member,
                    xproduct_id=item.product.id,
                    quantity=item.quantity,
                    price=xprice,
                    statusBuy=xstatusBuy,
                )
                order_member_item.save()
                #ลดจำนวน Stock
                # product=Opttran.objects.get(id=item.product.id)
                # product.stock=int(item.product.stock-order_item.quantity)
                # product.save()
                item.delete()
            return redirect('home')
        except Exception as e :
            pass
    
    return render(request,'checkout.html',dict(cart_items=cart_items,total=total,counter=counter))

def test(request):
    return render(request,'test.html')

def search(request):
    context = UpdMinicart(request)
    products=Product.objects.filter(name__contains=request.GET['title'])
    context['products'] = products

    return render(request,'shop.html',context)

def orderHistory(request):
    if request.user.is_authenticated:
        email=str(request.user.email)
        orders=OrderAllUser.objects.filter(email=email)
    
        context = UpdMinicart(request)
        context['orders'] = orders        
        
    return render(request,'orders.html',context)

def viewOrder(request,order_id):
    if request.user.is_authenticated:
        email=str(request.user.email)
        orders=OrderAllUser.objects.get(email=email,id=order_id)
        orderitem=OrderAllUserItem.objects.filter(order=orders)

        context = UpdMinicart(request)
        context['orders'] = orders
        context['order_items'] = orderitem

    return render(request,'vworder.html',context)

def contact(request):
    company = setContact.objects.get(id=1)
    context = UpdMinicart(request)
    context['company'] = company
    return render(request,'contact.html',context)

def index2(request):
    data1 = Pagesetting.objects.all().filter(flag=True,position='best_sell')[:8]
    data2 = Pagesetting.objects.all().filter(flag=True,position='band')[:2]
    data3 = Pagesetting.objects.all().filter(flag=True,position='recommend')[:8]
    context = {
        'data1': data1,
        'data2': data2,
        'data3': data3,
    }
    return render(request,'index-4.html',context)

def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("valid success")
            print("name"+form.cleaned_data['name'])
            print("Text"+form.cleaned_data['text'])

    return render(request, 'form_name.html',{'form': form})

def filter_dropdawn(request):
    car_form = StateForm()

    return render(request,'filter_dropdawn.html',{'car_form': car_form})

def vwSetgroup(request):
    context = {}
    groups = Setgroup.objects.all()
    subgroups = Setsubgroup.objects.all()
    typegroups = Settypegroup.objects.all()

    context['groups'] = groups
    context['subgroups'] = subgroups
    context['typegroups'] = typegroups

    return render(request,'vwSetgroup.html',context)

def vwSetsubgroup(request):
    context = {}
    group = request.GET.get('group')
    subgroups = Setsubgroup.objects.filter(group_id=group)
    context['subgroups'] = subgroups

    return render(request,'includes/_subgroup.html',context)

def vwSettypegroup(request):
    context = {}
    subgroup = request.GET.get('subgroup')

    typegroups = Settypegroup.objects.filter(subgroup_id=subgroup)
    context['typegroups'] = typegroups

    return render(request,'includes/_typegroup.html',context)

def vwDropdawn(request):
    context = {}
    groups = Setgroup.objects.all()
    subgroups = Setsubgroup.objects.all()
    typegroups = Settypegroup.objects.all()

    context['groups'] = groups
    context['subgroups'] = subgroups
    context['typegroups'] = typegroups

    return render(request,'vwDropdawn.html',context)

def vwDsubgroup(request):
    context = {}
    group = request.GET.get('group')
    subgroups = Setsubgroup.objects.filter(group_id=group)
    context['subgroups'] = subgroups

    return render(request,'includes/_Dsubgroup.html',context)

def vwDtypegroup(request):
    context = {}
    subgroup = request.GET.get('subgroup')
    typegroups = Settypegroup.objects.filter(subgroup_id=subgroup)
    context['typegroups'] = typegroups

    return render(request,'includes/_Dtypegroup.html',context)

def Delivery(request):
    context = UpdMinicart(request)
    qConditions = SetConditions.objects.filter(flag=True).order_by('orderNo')
    context['qConditions'] = qConditions
    return render(request,'delivery.html',context)

def workwithwe(request):
    context = UpdMinicart(request)
    qWork = setWorktogether.objects.filter(flag=True).order_by('orderNo')
    context['qWork'] = qWork
    return render(request,'workwithwe.html',context)

def ourservices(request):
    context = UpdMinicart(request)
    qWork = setOurservice.objects.filter(flag=True).order_by('orderNo')
    context['qWork'] = qWork
    return render(request,'ourservices.html',context)
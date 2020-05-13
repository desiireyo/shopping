"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shopone import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('shop/',views.shop,name='shop'),
    path('shop_promotion/',views.shop_promotion,name='shop_promotion'),
    path('product/<slug:group_slug>',views.indexSetgroup,name='product_by_group'),
    path('product/<slug:group_slug>/<slug:subgroup_slug>',views.indexSetsubgroup,name='product_by_subgroup'),
    path('product/<slug:group_slug>/<slug:subgroup_slug>/<slug:typegroup_slug>',views.indexSettypegroup,name='product_by_typegroup'),
    path('product/<slug:group_slug>/<slug:subgroup_slug>/<slug:typegroup_slug>/<slug:product_slug>',views.viewProduct,name="product_detail"),
    # path('product_pro/<slug:group_slug>',views.indexSetgroup,name='product_by_group'),
    # path('product_pro/<slug:group_slug>/<slug:subgroup_slug>',views.indexSetsubgroup,name='product_by_subgroup'),
    # path('product_pro/<slug:group_slug>/<slug:subgroup_slug>/<slug:typegroup_slug>',views.indexSettypegroup,name='product_by_typegroup'),
    # path('product_pro/<slug:group_slug>/<slug:subgroup_slug>/<slug:typegroup_slug>/<slug:product_slug>',views.viewProduct,name="product_detail"),
    path('cart/add/<int:product_id>',views.addCart,name="addCart"),
    path('cart/addx/',views.addCart2,name='addCart2'),
    path('cart/addx3/',views.addCart3,name='addCart3'),
    path('cart/remove/<int:product_id>',views.removeCart,name="removeCart"),
    path('cartdetail/',views.cartDetail,name="cartDetail"),
    path('UpdateCart/',views.UpdateCart,name="UpdateCart"),
    path('checkout/',views.checkout,name="checkout"),
    path('addOrderGuest/',views.addOrderGuest,name="addOrderGuest"),
    path('addOrderMember/',views.addOrderMember,name="addOrderMember"),
    path('account/Register',views.Register,name="Register"),
    path('account/Login',auth_views.LoginView.as_view(template_name='login.html'),name="Login"),
    path('account/Loout',auth_views.LogoutView.as_view(template_name='logout.html'),name="Logout"),
    path('search/',views.search, name='search'),
    path('orderHistory/',views.orderHistory, name='orderHistory'),
    path('order/<int:order_id>',views.viewOrder,name='viewOrder'),
    path('contact/',views.contact, name='contact'),
    path('Delivery/',views.Delivery,name='Delivery'),
    path('workwithwe/',views.workwithwe,name='workwithwe'),
    path('ourservices/',views.ourservices,name='ourservices'),

    path('updateCart/',views.UpdMinicart,name='UpdMinicart'),


    path('',include('mysetting.urls')),

    path('test/',views.test,name='test'),
    path('test2/',views.index2,name='test2'),
    path(r'formpage/',views.form_name_view,name='form_name'),
    path('filter_dropdawn/',views.filter_dropdawn,name='filter_dropdawn'),
    path('vwSetgroup/',views.vwSetgroup,name='vwSetgroup'),
    path('vwSetsubgroup/',views.vwSetsubgroup,name='vwSetsubgroup'),
    path('vwSettypegroup/',views.vwSettypegroup,name='vwSettypegroup'),

    path('vwDropdawn/',views.vwDropdawn,name='vwDropdawn'),
    path('vwDsubgroup/',views.vwDsubgroup,name='vwDsubgroup'),
    path('vwDtypegroup/',views.vwDtypegroup,name='vwDtypegroup'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

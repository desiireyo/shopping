from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard',mysetting,name='mysetting'),
    path('customize/setgroup',mysetgroup,name="mysetgroup"),
    path('customize/setgroup/createSetgroup',createSetgroup,name="createSetgroup"),
    path('customize/setgroup/addSetgroup',addSetgroup,name="addSetgroup"),
    path('customize/setgroup/editSetgroup/<int:group_id>',editSetgroup,name="editSetgroup"),
    path('customize/setgroup/updSetgroup',updSetgroup,name="updSetgroup"),
    path('customize/setgroup/delSetgroup/<int:group_id>',delSetgroup,name="delSetgroup"),

    path('customize/setunit',mysetunit,name="mysetunit"),
    path('customize/setunit/createSetunit',createSetunit,name="createSetunit"),
    path('customize/setunit/addSetunit',addSetunit,name="addSetunit"),
    path('customize/setunit/editSetunit/<int:unit_id>',editSetunit,name="editSetunit"),
    path('customize/setunit/updSetunit',updSetunit,name="updSetunit"),
    path('customize/setunit/delSetunit/<int:unit_id>',delSetunit,name="delSetunit"),

    path('customize/setstatus',mysetstatus,name="mysetstatus"),
    path('customize/setstatus/createSetstatus',createSetstatus,name="createSetstatus"),
    path('customize/setstatus/addSetstatus',addSetstatus,name="addSetstatus"),
    path('customize/setstatus/editSetstatus/<int:status_id>',editSetstatus,name="editSetstatus"),
    path('customize/setstatus/updSetstatus',updSetstatus,name="updSetstatus"),
    path('customize/setstatus/delSetstatus/<int:status_id>',delSetstatus,name="delSetstatus"),

    path('customize/setsubgroup',SetsubgroupListView.as_view(),name="mysetsubgroup"),
    path('customize/setsubgroup/create', SetsubgroupCreateView.as_view(), name='mysetsubgroup-create'),
    path('customize/setsubgroup/update/<int:pk>', SetsubgroupUpdateView.as_view(), name='mysetsubgroup-update'),
    path('customize/setsubgroup/delete/<int:group_id>', SetsubgroupDeleteView, name='mysetsubgroup-delete'),

    path('customize/settypegroup',mysettypegroup,name="mysettypegroup"),
    path('customize/settypegroup/create',createSettypegroup,name="createSettypegroup"),
    path('customize/settypegroup/addSettypegroup',addSettypegroup,name="addSettypegroup"),
    path('customize/settypegroup/edit/<int:settypegroup_id>',editSettypegroup,name="editSettypegroup"),
    path('customize/settypegroup/update',updSettypegroup,name="updSettypegroup"),
    path('customize/settypegroup/delete/<int:settypegroup_id>',delSettypegroup,name="delSettypegroup"),

    path('customize/myproduct',myproduct,name="myproduct"),
    path('customize/myproduct/create',createProduct,name="createProduct"),
    path('customize/myproduct/addProduct',addProduct,name="addProduct"),
    path('customize/myproduct/edit/<int:product_id>',editProduct,name="editProduct"),
    path('customize/myproduct/update',updProduct,name="updProduct"),
    path('customize/myproduct/delete/<slug:product_slug>',delProduct,name="delProduct"),

    path('customize/picproduct',picproduct,name="picproduct"),
    path('customize/picproduct/create',createPicProduct,name="createPicProduct"),
    path('customize/picproduct/PicProduct',addPicProduct,name="addPicProduct"),
    path('customize/picproduct/edit/<int:productimage_id>',editProductImage,name="editProductImage"),
    path('customize/picproduct/update',updProductImg,name="updProductImg"),
    path('customize/picproduct/delete/<int:productimg_id>',delProductImg,name="delProductImg"),

    path('myorder/member',myOrdermember,name="myOrdermember"),
    path('myorder/confirm/<int:order_id>',confirmOrdermember,name='confirmOrdermember'),
    path('myorder/canconfirm/<int:order_id>',CanconfirmOrdermember,name='CanconfirmOrdermember'),

    path('myorder/guest',myOrderguest,name="myOrderguest"),
    path('myorder/guest/confirm/<int:order_id>',confirmOrderguest,name='confirmOrderguest'),
    path('myorder/guest/canconfirm/<int:order_id>',CanconfirmOrderguest,name='CanconfirmOrderguest'),

    path('myorder/myorderall',myOrderall,name="myOrderall"),
    path('myorder/report',rp_myorder,name="rp_myorder"),

    path('pageset/pagehomeSetting',pagehomeSetting,name="pagehomeSetting"),
    path('pageset/pagehomeSetting/create',createNewband,name="createNewband"),
    path('pageset/pagehomeSetting/add',addNewband,name="addNewband"),
    path('pageset/pagehomeSetting/edit/<int:position_id>',editBand,name="editBand"),
    path('pageset/pagehomeSetting/update',updBand,name="updBand"),
    path('pageset/pagehomeSetting/delete/<int:position_id>',delBand,name="delBand"),

    path('pageset/pagebestSell',pagebestSell,name="pagebestSell"),
    path('pageset/pagebestSell/create',createNewbestsell,name="createNewbestsell"),
    path('pageset/pagebestSell/add',addNewbestsell,name="addNewbestsell"),
    path('pageset/pagebestSell/edit/<int:position_id>',editBestsell,name="editBestsell"),
    path('pageset/pagebestSell/update',updBestsell,name="updBestsell"),
    path('pageset/pagebestSell/delete/<int:position_id>',delBestsell,name="delBestsell"),

    path('pageset/pagerecommend',pagerecommend,name="pagerecommend"),
    path('pageset/pagerecommend/create',createNewrecommand,name="createNewrecommand"),
    path('pageset/pagerecommend/add',addNewrecommand,name="addNewrecommand"),
    path('pageset/pagerecommend/edit/<int:position_id>',editRecommand,name="editRecommand"),
    path('pageset/pagerecommend/update',updRecommand,name="updRecommand"),
    path('pageset/pagerecommend/delete/<int:position_id>',delRecommand,name="delRecommand"),

    path('pageset/pagepromotion',pagepromotion,name="pagepromotion"),
    path('pageset/pagepromotion/create',createNewpromotion,name="createNewpromotion"),
    path('pageset/pagepromotion/add',addNewpromotion,name="addNewpromotion"),
    path('pageset/pagepromotion/edit/<int:position_id>',editPromotion,name="editPromotion"),
    path('pageset/pagepromotion/update',updPromotion,name="updPromotion"),
    path('pageset/pagepromotion/delete/<int:position_id>',delPromotion,name="delPromotion"),

    path('pageset/pageconditions',SetCondition,name='SetCondition'),
    path('pageset/pageconditions/add',AddConditions,name="AddConditions"),
    path('pageset/pageconditions/create',CreateConditions,name="CreateConditions"),
    path('pageset/pageconditions/edit/<int:page_id>',EditConditions,name="EditConditions"),
    path('pageset/pageconditions/update',UpdConditions,name="UpdConditions"),
    path('pageset/pageconditions/delete/<int:page_id>',DelConditions,name="DelConditions"),

    path('pageset/pagepromotion2',SetProducttoPromotion,name='SetProducttoPromotion'),
    path('pageset/pagepromotion2/add',AddProducttoPromotion,name="AddProducttoPromotion"),
    path('pageset/pagepromotion2/create',CreateProducttoPromotion,name="CreateProducttoPromotion"),
    path('pageset/pagepromotion2/edit/<int:page_id>',EditPromotion2,name="EditPromotion2"),
    path('pageset/pagepromotion2/update',UpdPromotion2,name="UpdPromotion2"),
    path('pageset/pagepromotion2/delete/<int:page_id>',DelPromotion2,name="DelPromotion2"),

    path('customize/setshipping',ShippingPrice,name="ShippingPrice"),
    path('customize/setshipping/create',createShippingPrice,name="createShippingPrice"),
    path('customize/setshipping/add',addNewshipping,name="addNewshipping"),
    path('customize/setshipping/edit/<int:shipping_id>',editShipping,name="editShipping"),
    path('customize/setshipping/update',updShipping,name="updShipping"),
    path('customize/setshipping/delete/<int:shipping_id>',delShipping,name="delShipping"),

    path('myDropdawn/',myDropdawn,name='myDropdawn'),
    path('myDsubgroup/',myDsubgroup,name='myDsubgroup'),
    path('myDtypegroup/',myDtypegroup,name='myDtypegroup'),

    path('customize/picproduct/addpic', BasicUploadView.as_view(), name='addPic-create'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
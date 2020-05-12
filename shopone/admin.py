from django.contrib import admin
from shopone.models import Setgroup,Setsubgroup,Settypegroup,Setunit,Setstatus,Product,ProductImageItem,Cart,CartItem,OrderGuest,OrderGuestItem,Pagesetting

# Register your models here.

admin.site.register(Setgroup)
admin.site.register(Setsubgroup)
admin.site.register(Settypegroup)
admin.site.register(Setunit)
admin.site.register(Setstatus)
admin.site.register(Product)
admin.site.register(ProductImageItem)

admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(OrderGuest)
admin.site.register(OrderGuestItem)

admin.site.register(Pagesetting)
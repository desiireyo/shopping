from shopone.models import Product,Setgroup,Setsubgroup,Settypegroup,Setunit,Setstatus
# from shopone.views import _cart_id

def menu_setgroup(request):
    setgroups=Setgroup.objects.all()
    return dict(setgroups=setgroups)

def menu_setsubgroup(request):
    setgroups=Setgroup.objects.all()
    setsubgroups=Setsubgroup.objects.all()
    return dict(setsubgroups=setsubgroups)

def menu_settypegroup(request):
    settypegroups=Settypegroup.objects.all()
    return dict(settypegroups=settypegroups)
from django.contrib import admin

from dashboard.models import Cart,CartItem,Post,MpesaPayment

# Register your models here.
admin.site.register( Cart)
admin.site.register(CartItem)
admin.site.register(Post)
admin.site.register(MpesaPayment)

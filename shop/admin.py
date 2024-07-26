from django.contrib import admin
from shop.models import User, Bid, ItemUpdated, ItemUserConnect, Comment




class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)

class BidAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bid, BidAdmin)

class ItemUpdatedAdmin(admin.ModelAdmin):
    pass

admin.site.register(ItemUpdated, ItemUpdatedAdmin)

class ItemUserConnectAdmin(admin.ModelAdmin):
    pass

admin.site.register(ItemUserConnect, ItemUserConnectAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)

# Register your models here.

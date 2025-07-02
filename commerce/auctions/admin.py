from django.contrib import admin
from .models import User, Item, Bid, Category, Comment

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'starting_bid', 'isopen', 'category', 'owner')
    list_filter = ('isopen', 'category', 'owner')
    search_fields = ('title', 'description')
    raw_id_fields = ('owner', 'category')

class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'amount', 'bidder', 'timestamp')
    list_filter = ('item', 'bidder')
    raw_id_fields = ('item', 'bidder')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'by', 'text', 'like')
    list_filter = ('item', 'by')
    search_fields = ('text',)
    raw_id_fields = ('item', 'by')


admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
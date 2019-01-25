from django.contrib import admin

from .models import Item, Variant, VariantProperty, ItemChangeLog, VariantChangeLog

admin.site.register(Item)
admin.site.register(Variant)
admin.site.register(VariantProperty)
admin.site.register(ItemChangeLog)
admin.site.register(VariantChangeLog)


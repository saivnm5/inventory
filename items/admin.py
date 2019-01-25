from django.contrib import admin

from .models import Item, Variant, VariantPropery, ItemChangeLog, VariantChangeLog

admin.site.register(Item)
admin.site.register(Variant)
admin.site.register(VariantPropery)
admin.site.register(ItemChangeLog)
admin.site.register(VariantChangeLog)


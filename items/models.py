from django.db import models

class Item(models.Model):
	name = models.CharField(max_length=255)
	brand = models.CharField(max_length=255)
	category = models.CharField(max_length=255)
	product_code = models.CharField(max_length=13)


class Variant(models.Model):
	item = models.ForeignKey(Item, on_delete=models.PROTECT)
	name = models.CharField(max_length=255)
	selling_price = models.DecimalField(max_digits=6, decimal_places=2)
	cost_price = models.DecimalField(max_digits=6, decimal_places=2)
	quantity = models.IntegerField()
	is_active = models.BooleanField(default=True)


class VariantPropery(models.Model):
	# using EAV model
	variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
	property = models.CharField(max_length=255)
	value = models.CharField(max_length=255)


class ItemChangeLog(models.Model):
	item = models.ForeignKey(Item, on_delete=models.PROTECT)
	attribute = models.CharField(max_length=255)
	is_variant = models.BooleanField(default=False)
	old_value = models.CharField(max_length=255)
	new_value = models.CharField(max_length=255)
	user = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)


class VariantChangeLog(models.Model):
	variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
	attribute = models.CharField(max_length=255)
	is_property = models.BooleanField(default=False)
	old_value = models.CharField(max_length=255)
	new_value = models.CharField(max_length=255)
	user = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
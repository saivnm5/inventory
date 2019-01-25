from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker


class Item(models.Model):
	name = models.CharField(max_length=255)
	brand = models.CharField(max_length=255)
	category = models.CharField(max_length=255)
	product_code = models.CharField(max_length=13)
	# last_user
	tracker = FieldTracker()

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


@receiver(post_save, sender=Item)
def item_change_logger(sender, instance, created, raw, using, update_fields, **kwargs):
	
	if not created:
		if instance.tracker.has_changed('name'):
			log = ItemChangeLog(item=instance, attribute='name', user='ghost')
			log.old_value = instance.name 
			log.new_value = instance.tracker.previous('name')
			log.save()

		if instance.tracker.has_changed('brand'):
			log = ItemChangeLog(item=instance, attribute='brand', user='ghost')
			log.old_value = instance.brand 
			log.new_value = instance.tracker.previous('brand')
			log.save()

		if instance.tracker.has_changed('category'):
			log = ItemChangeLog(item=instance, attribute='category', user='ghost')
			log.old_value = instance.category 
			log.new_value = instance.tracker.previous('category')
			log.save()